from Connector import Connector


class ConnectorResource:

    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):

        self.connector = Connector(self.db_name)
        return self.connector

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connector.disconnect()
