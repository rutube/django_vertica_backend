# coding: utf-8

# $Id: $
import os
import mock
import pyodbc
from unittest import TestCase
from vertica.base import Database, DatabaseWrapper

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_app.settings")
from test_app.models import PlatformReport


class VerticaBackendTestCase(TestCase):
    def setUp(self):
        self.cursor_mock = mock.MagicMock()
        self.connect_patcher = mock.patch.object(Database, 'connect')
        self.connect_patcher.start()
        self.cursor_patcher = mock.patch.object(DatabaseWrapper, 'cursor',
                                                return_value=self.cursor_mock)
        self.cursor_patcher.start()
        self.fetchmany_patcher = mock.patch.object(self.cursor_mock,
                           'fetchmany', side_effect=StopIteration())
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
        self.cursor_mock.execute.assertCalledWith([self.query, ()])

    def testLimitOffset(self):
        list(PlatformReport.objects.all()[100:500])
        query = self.query + " LIMIT ? OFFSET ?"
        self.cursor_mock.execute.assertCalledWith([query, (500, 100)])
