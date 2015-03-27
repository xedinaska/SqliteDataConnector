#!/usr/bin/python
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from ConnectorResource import ConnectorResource
import json

PORT_NUMBER = 8081


class Object:
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):

    #Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        request = self.path.split('&')[1:]
        request_data = {}

        for pair in request:
            pair_parts = pair.split('=')
            request_data[pair_parts[0]] = pair_parts[1]
        print(request_data)

        # Send the html message
        with ConnectorResource('../sqlite_db/main.db') as connector:
            if request_data.get('action') == 'get_tables':
                self.wfile.write(bytes(json.dumps(connector.get_tables()), "utf-8"))
            elif request_data.get('action') == 'load_table_structure':
                table_structure = connector.get_table_structure(request_data.get('table_name'))
                self.wfile.write(bytes(json.dumps(table_structure), "utf-8"))
            elif request_data.get('action') == 'load_table_content':
                table_content = connector.get_table_content(request_data.get('table_name'))
                self.wfile.write(bytes(json.dumps(table_content, indent=2), "utf-8"))
            else:
                self.wfile.write(bytes(json.dumps([]), "utf-8"))
        return


try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print('Started httpserver on port ', PORT_NUMBER)

    #Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()