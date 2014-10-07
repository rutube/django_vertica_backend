# coding: utf-8

from django.conf import settings
from django.db.models.sql.compiler import *

# Vertica doesn't validate constraints when data are loaded into a table.
# Constraints violation will cause errors at run time.
# This flag enforces constraints validation after data inserting.
# Maybe, it's usefull to validate constraints after updating or deleting, too?
ENFORCE_CONSTRAINTS_VALIDATION = getattr(settings, "ENFORCE_CONSTRAINTS_VALIDATION", True)


class SQLInsertCompiler(SQLInsertCompiler):

    def execute_sql(self, return_id=False):
        result = super(SQLInsertCompiler, self).execute_sql(return_id)

        if ENFORCE_CONSTRAINTS_VALIDATION:
            self.connection.ops.validate_constraints(
                self.connection.cursor(),
                self.query.get_meta().db_table)

        return result