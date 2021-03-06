# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
import json
import time

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
            userInput = raw_input("")
            liste = []
            if " " in userInput:
                content = ""
                liste = userInput.split(" ")
                request = liste[0]
                for i in range(1, len(liste)):
                    content += liste[i]
                    if(i != len(liste)-1):
                        content += " "
            else:
                request = userInput
                content = None

            self.send_payload(request, content)
            if request == "logout":
                self.disconnect()

            reciever = MessageReceiver(self, self.connection)
            reciever.daemon = True
            reciever.start()


        
    def disconnect(self):
        self.connection.shutdown(socket.SHUT_RDWR)

    def receive_message(self, message):
        parser = MessageParser()
        messageType = parser.parse(message)
        print messageType


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
    client = Client('10.20.54.145', 30000)
