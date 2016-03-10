# -*- coding: utf-8 -*-
import SocketServer
import json
import time
import datetime

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

users = {}
username = ""

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """


    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        print 'client connected'

        # Loop that listens for messages from the client
        while True:


            received_string = self.connection.recv(4096)
            # TODO: Add handling of received payload from client
            recieved_content = json.loads(received_string)
            print 'after json.loads'
            request = recieved_content['request']
            payload = recieved_content['content']

            if request == "login":
                print 'request located'
                self.login(payload)
            elif request == "logout":
                self.logout()
            elif request == "message":
                self.message(payload)
            elif request == "listNames":
                self.listNames()
            elif request == "help":
                self.handleHelp()
            else:
                self.handleError("Incorrect command!")

    def login(self, payload):
        if not payload in users:
            print 'request processed'
            users[payload] = self
            username = payload
            self.handleResponse("message", "You successfully logged in!")
            print 'user logged in on server'
        else:
            self.handleError("Error: This user is already logged in...")
            print 'user was already logged in'

    def logout(self):
        if(username in users):
            users.pop(username)

    def message(self, payload):
        pass

    def listNames(self):
        pass

    def handleHelp(self):
        pass

    def handleResponse(self, response, content):
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
        data = {'timestamp':st,'sender':username,'response':response,'content':content}
        package = json.dumps(data)
        print users
        self.connection.send(package)

    def handleError(self, errorType):
        self.handleResponse("error", errorType)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()