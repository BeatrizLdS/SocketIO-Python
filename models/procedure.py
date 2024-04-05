import json
from models.move import Move
from models.chat_message import ChatMessage

class Procedure:
    def __init__(self, procedure, parameters):
        self.procedure = procedure
        self.parameters = parameters
        
    @classmethod
    def decode(self, json_data):
        decoded_data = json.loads(json_data)
        procedure = decoded_data['procedure']
        
        if procedure == 'message':
            parameters = ChatMessage.decode(decoded_data['parameters'])
        else:
            parameters = Move.decode(decoded_data['parameters']) 
        
        return Procedure(procedure, parameters)
    
    def execute(self):
        if self.procedure == 'message':
            new_message = ChatMessage.change_sender(self.parameters)
            return json.dumps(self.parameters.__dict__), json.dumps(new_message.__dict__)
        else:
            new_move = Move.executeMove(self.parameters)
            return json.dumps(self.parameters.__dict__), json.dumps(new_move.__dict__)