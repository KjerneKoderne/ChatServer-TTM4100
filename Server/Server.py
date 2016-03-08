# -*- coding: utf-8 -*-
import SocketServer
import json
import time

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

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            # TODO: Add handling of received payload from client
            recieved_content = json.loads(received_string)

            request = recieved_content['request']
            payload = recieved_content['content']

            if request == "login":
            	login(payload)
            elif request == "logout":
            	logout()
            elif request == "message":
            	message(payload)
            elif request == "listNames":
            	listNames()
            elif request == "help":
            	handleHelp()
            else:
                handleError()

    def login(payload):
        if not payload in users:
            users[payload] = self
            self.username = payload
            handleResponse("message", "User" + payload + "successfully logged in!")
        else:
            handleError("Error: This user is already logged in...")

    def logout():
        if 

    def message(payload):
        pass

    def listNames():
        pass

    def handleHelp():
        pass

    def handleResponse(response, content):
        data = {'timestamp':time.time(),'sender':username 'response':response,'content':content}
        payload = json.dumps(data)
        self.connection.send(payload)

    def handleError(errorType):
        pass


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
