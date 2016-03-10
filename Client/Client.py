# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
import json

request = ""
content = ""
data = ""

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # TODO: Finish init process with necessary code
        self.host = host
        self.server_port = server_port
        self.run()

    def run(self):
        # Initiate the connection to the server

        self.connection.connect((self.host, self.server_port))

        while True:
            userInput = raw_input("Choose command:")
            liste = []
            if " " in userInput:
                liste = userInput.split(" ")
                request = liste[0]
                content = liste[1]
            else:
                request = userInput
                content = None

            self.send_payload(request, content)
            self.reciever = MessageReceiver(self , self.connection)

        
    def disconnect(self):
        # TODO: Handle disconnection
        pass

    def receive_message(self, message):
        pass

    def send_payload(self, request, content):
        # TODO: Handle sending of a payload
        data = {'request':request,'content':content}
        payload = json.dumps(data)
        self.connection.send(payload)
    # More methods may be needed!
        


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
