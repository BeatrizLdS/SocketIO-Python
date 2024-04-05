
class ChatMessage:
    def __init__(self, sender, content):
        self.sender = sender
        self.content = content
    
    @classmethod
    def decode(self, json):
        sender = json['sender']
        content = json['content']
        return ChatMessage(sender, content)
    
    @classmethod
    def change_sender(self, original_message):
        content = original_message.content
        sender = 'remoteUser' if original_message.sender == 'localUser' else 'localUser'
        return ChatMessage(sender, content)

