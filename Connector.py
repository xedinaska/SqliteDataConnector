import sqlite3


class Connector:

    connection = None
    required_fields = None

    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.required_fields = {
            'Accounts': ['id', 'skypename', 'fullname', 'languages', 'country', 'city', 'emails', 'mood_text'],
            'Alerts': ['id', 'is_permanent', 'timestamp', 'is_unseen', 'partner_id', 'message_header_caption',
                       'message_content', 'message_footer'],
            'Calls': ['id', 'host_identity', 'duration', 'soundlevel', 'is_incoming', 'current_video_audience'],
            'CallMembers': ['id', 'identity', 'dispname'],
            'ContactGroups': ['id', 'type'],
            'Contacts': ['id', 'skypename', 'fullname', 'country', 'city', 'phone_mobile', 'mood_text',
                         'popularity_ord', 'pop_score'],
            'Chats': ['id', 'friendlyname', 'timestamp', 'conv_dbid'],
            'Conversations': ['id', 'type', 'displayname', 'last_activity_timestamp'],
            'Messages': ['id', 'convo_id', 'from_dispname', 'timestamp', 'body_xml'],
            'Participants': ['id', 'convo_id', 'identity', 'rank'],
            'SMSes': ['id'],
            'Transfers': ['id', 'type', 'partner_dispname', 'status', 'starttime', 'finishtime', 'filename'],
            'VideoMessages': ['id'],
            'Videos': ['id'],
            'Voicemails': ['id']
        }

    def disconnect(self):
        self.connection.close()

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

    def get_table_structure(self, table_name):
        cur = self.connection.cursor()

        cur.execute('PRAGMA table_info(' + table_name + ')')

        table_fields = []

        for table_field in cur.fetchall():
            if table_name in self.required_fields:
                if table_name == 'Chats':
                    print(table_field[1])
                if table_field[1] in self.required_fields.get(table_name):
                    table_fields.append(table_field[1])
            else:
                table_fields.append(table_field[1])

        return table_fields

    def get_table_content(self, table_name):
        cur = self.connection.cursor()
        select_string = '*'

        if table_name in self.required_fields:
            fields = self.required_fields.get(table_name)
            select_string = ",".join(fields)

        cur.execute('SELECT ' + select_string + ' FROM main.' + table_name + ' LIMIT 100')

        return cur.fetchall()