from ConnectorResource import ConnectorResource
import json

with ConnectorResource('sqlite_db/main.db') as connector:
    print(json.dumps(connector.get_tables()))
    #print(connector.get_tables())
    #print(connector.get_table_fields('Chats'))
    connector.get_table_content('Chats')
    #for chat in chats:
        #for value in chat:
            #if isinstance(value, bytes):
                #value.decode()
               #print(str(value))
            #2print(value.decode('ascii'))
