# coding: utf-8

# $Id: $
from django import VERSION
from django.db import transaction

import mock
from django.db.models import Sum
from django.test import TestCase
from django.test.simple import DjangoTestSuiteRunner

from vertica.base import Database, DatabaseWrapper
from test_app.models import PlatformReport


class VerticaTestRunner(DjangoTestSuiteRunner):
    '''TestRunner с отключенным созданием и удалением БД.'''

    def setup_databases(self, *args, **kwargs):
        '''Настраивает БД перед запуском тестов.'''
        return ([], [])

    def teardown_databases(self, *args, **kwargs):
        '''Откатывает БД после выполнения тестов.'''
        pass


class VerticaBackendTestCase(TestCase):


    def _fixture_setup(self):
        pass

    def _fixture_teardown(self):
        pass

    def setUp(self):
        self.cursor_mock = mock.MagicMock()
        self.connect_mock = mock.MagicMock()
        self.connect_patcher = mock.patch.object(Database, 'connect',
                                                 return_value=self.connect_mock)
        self.connect_patcher.start()
        self.cursor_patcher = mock.patch.object(DatabaseWrapper, 'cursor',
                                                return_value=self.cursor_mock)
        self.cursor_patcher.start()
        self.fetchmany_patcher = mock.patch.object(self.cursor_mock,
                                                   'fetchmany',
                                                   side_effect=StopIteration())
        self.fetchmany_patcher.start()

        self.query = (u'SELECT "reports_platformreport"."id", '
                      u'"reports_platformreport"."date", '
                      u'"reports_platformreport"."platform_id", '
                      u'"reports_platformreport"."video_id", '
                      u'"reports_platformreport"."video_views", '
                      u'"reports_platformreport"."adv_views", '
                      u'"reports_platformreport"."income", '
                      u'"reports_platformreport"."approved" '
                      u'FROM "reports_platformreport"')

    def tearDown(self):
        self.connect_patcher.stop()
        self.cursor_patcher.stop()
        self.fetchmany_patcher.stop()

    def testConnection(self):
        list(PlatformReport.objects.all())
        self.cursor_mock.execute.assert_called_with(self.query, ())

    def testLimitOffset(self):
        list(PlatformReport.objects.all()[100:500])
        query = self.query + " LIMIT 400 OFFSET 100"
        self.cursor_mock.execute.assert_called_with(query, ())

    def testGroupBy(self):
        qs = PlatformReport.objects.filter(date__gte='2014-09-15')
        qs = qs.values('platform_id')
        qs = qs.annotate(video_views=Sum('video_views'))
        list(qs[100:500])
        query = ('SELECT "reports_platformreport"."platform_id", '
                 'SUM("reports_platformreport"."video_views") AS "video_views" '
                 'FROM "reports_platformreport" '
                 'WHERE "reports_platformreport"."date" >= %s ')
        if VERSION < (1, 7, 0):
            query += ' '
        query += ('GROUP BY "reports_platformreport"."platform_id" '
                  'LIMIT 400 OFFSET 100')
        self.cursor_mock.execute.assert_called_with(query, (u'2014-09-15',))

    def testAutocommit(self):
        from django.db import connection
        connection.set_autocommit(False)
        self.connect_mock.query.assert_called_with('SET SESSION AUTOCOMMIT TO OFF')
        connection.set_autocommit(True)
        self.connect_mock.query.assert_called_with('SET SESSION AUTOCOMMIT TO ON')
