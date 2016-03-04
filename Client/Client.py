# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

request = ""
content = ""
data = ""
payload = ""

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
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))

        userInput = raw_input("Choose command:")
        liste = []
        if " " in userInput:
            liste = userInput.split(" ")
            request = liste[0]
            content = liste[1]
        else:
            request = userInput
            content = ""

        
    def disconnect(self):
        # TODO: Handle disconnection
        pass

    def receive_message(self, message):
        # TODO: Handle incoming message
        pass

    def send_payload(self, data):
        # TODO: Handle sending of a payload
        payload = json.dumps(data)
        self.connection.send(payload)
    
    # More methods may be needed!

    def createPayload(request, content):
        #eks. login(username) -> request(content)
        #skal gjøres om til json format og dumpes i payload.txt for sending
        data = {'request':request,'content':content}    
        


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
