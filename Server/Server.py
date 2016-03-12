# -*- coding: utf-8 -*-
import SocketServer
import json
import time
import datetime
import re
 
"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

users = {}
user_ip = {}
username = ""
messageList = []

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
            elif request == "help":
                self.handleHelp()
            elif request == "logout" and self in users.values():
                self.logout()
            elif request == "msg" and self in users.values():
                self.message(payload)
            elif request == "names" and self in users.values():
                self.listNames()
            else:
                self.handleError("Incorrect command! Type 'help' for commands")

    def login(self, payload):

        if not payload in users and not self in users.values():
            if re.match("^[A-Za-z0-9]*$", payload):
                print 'request processed'
                users[payload] = self
                self.username = payload
                user_ip[self.ip] = username
                self.handleResponse("info", "You successfully logged in!")
                print 'user logged in on server'
                history = ""
                if(len(messageList)>0):
                    for message in messageList:
                        history += message
                    self.handleResponse("history", history)
            else:
                self.handleError("Error: Your username is not valid, please use only characters or numbers...")
                print 'invalid username'
        else:
            self.handleError("Error: You can only log on as one user...")
            print 'user was already logged in'

    def logout(self):
        if self in users.values():
            self.handleResponse("info", "You've successfully logged out!")
            users.pop(self.username, None)
        else:
            self.handleError("Error: Your logout did not succeed...")

    def message(self, payload):
        print 'request processed'
        self.sendMessage("message", payload)

    def listNames(self):
        listOfNames = ""
        tempArray = users.keys()
        for names in tempArray:
            listOfNames += names
            listOfNames += "\n"
        self.handleResponse("info", listOfNames)
        print 'user ' + self.username + ' requested list of logged in users.'


    def handleHelp(self):
        listOfCommands = "login <username>\nlogout\nmsg <message>\nnames\nhelp"
        self.handleResponse("info", listOfCommands)

    def handleResponse(self, response, content):
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
        data = {'timestamp':st,'sender':self.username,'response':response,'content':content}
        package = json.dumps(data)
        self.connection.send(package)

    def sendMessage(self, response, content):
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
        data = {'timestamp':st,'sender':self.username,'response':response,'content':content}
        package = json.dumps(data)
        messageList.append("[" + st + "] " + self.username + ": " + content + "\n")
        for value in users.values():
            value.connection.send(package)

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
    HOST, PORT = '', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()