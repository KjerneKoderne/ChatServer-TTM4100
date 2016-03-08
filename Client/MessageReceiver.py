# -*- coding: utf-8 -*-
from threading import Thread

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """

        # Flag to run thread as a deamon
        self.daemon = True

        # TODO: Finish initialization of MessageReceiver
        print'init MessageReceiver'

    def run(self):
        # TODO: Make MessageReceiver receive and handle payloads

        received_string = self.connection.recv(4096)
        recieved_content = json.loads(received_string)
        print 'after json.loads client'

        timestamp = recieved_content['timestamp']
        sender = recieved_content['sender']
        response = recieved_content['response']
        content = recieved_content['content']
