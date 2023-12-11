class Message_stack:
    def __init__(self):
        self.messages = []
        self.messages_by_sender = {}


    def add(self, message):
        self.messages.append(message)
        ### add messages by sender noch implementieren