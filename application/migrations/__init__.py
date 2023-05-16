from django.db.migrations.operations.base import Operation


class CreatorSchema(Operation):
    reversible = True

    def __init__(self, name):
        self.name = name

    def state_forwards(self, app_label, state):
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        schema_editor.execute("CREATE SCHEMA IF NOT EXISTS %s" % self.name)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        schema_editor.execute("DROP SCHEMA IF EXISTS %s CASCADE" % self.name)

    def describe(self):
        return "Creates schema %s" % self.name

    @property
    def migration_name_fragment(self):
        return "create_schema_%s" % self.name
