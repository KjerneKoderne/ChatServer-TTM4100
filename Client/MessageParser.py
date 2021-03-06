import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history,
	    # More key:values pairs are needed	
        }

    def parse(self, payload):
        payload = json.loads(payload)
    
        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            #throw error
            pass

    def parse_error(self, payload):
        return payload['content'] + "\n"
    
    def parse_info(self, payload):
        return payload['content'] +"\n"

    def parse_message(self, payload):
        return "[" + payload['timestamp'] + "] " + payload['sender'] + ": " + payload['content']

    def parse_history(self, payload):
        history = ""
        for element in payload['content']:
            dictionary = json.loads(element)
            history += "[" + dictionary['timestamp'] + "] " + dictionary['sender'] + ": " + dictionary['content'] + "\n"
        return history
        
    # Include more methods for handling the different responses... 
