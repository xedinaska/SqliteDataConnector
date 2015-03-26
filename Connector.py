import sqlite3
import json


class Connector:

    connection = None
    required_fields = None
    fields_to_fetch = 'config/fields.json'

    #init db connection
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)

        with open(self.fields_to_fetch) as json_data:
            self.required_fields = json.load(json_data)

    #close db connection
    def disconnect(self):
        self.connection.close()

    #get db tables list
    def get_tables(self):
        cur = self.connection.cursor()

        cur.execute('SELECT name FROM main.sqlite_master WHERE type="table"')

        tables = []

        for table in cur.fetchall():
            table_name = str(table)
            table_name = table_name.replace("('", '')
            table_name = table_name.replace("',)", '')
            tables.append(table_name)

        return tables

    #get db table fields list
    def get_table_structure(self, table_name):
        cur = self.connection.cursor()

        cur.execute('PRAGMA table_info(' + table_name + ')')

        table_fields = []

        for table_field in cur.fetchall():
            if table_name in self.required_fields:
                if table_field[1] in self.required_fields.get(table_name):
                    table_fields.append(table_field[1])
            else:
                table_fields.append(table_field[1])

        return table_fields

    #get db table content data
    def get_table_content(self, table_name):
        cur = self.connection.cursor()
        select_string = '*'

        if table_name in self.required_fields:
            fields = self.required_fields.get(table_name)
            select_string = ",".join(fields)

        cur.execute('SELECT ' + select_string + ' FROM main.' + table_name + ' ')

        return cur.fetchall()