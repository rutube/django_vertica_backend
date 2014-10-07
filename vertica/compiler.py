# coding: utf-8

from django.db.models.sql.compiler import *


class SQLInsertCompiler(SQLInsertCompiler):

    def execute_sql(self, return_id=False):
        assert not (return_id and len(self.query.objs) != 1)
        self.return_id = return_id
        cursor = self.connection.cursor()
        for sql, params in self.as_sql():
            cursor.execute(sql, params)

        self.connection.ops.validate_constraints(
            cursor, self.query.get_meta().db_table)

        if not (return_id and cursor):
            return
        if self.connection.features.can_return_id_from_insert:
            return self.connection.ops.fetch_returned_insert_id(cursor)
        return self.connection.ops.last_insert_id(cursor,
                self.query.get_meta().db_table, self.query.get_meta().pk.column)