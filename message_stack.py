class Message_Stack:
    def __init__(self):
        self.messages = []
        self.messages_by_sender = {}

    def add(self, message):
        self.messages.append(message)
        ### add messages by sender noch implementieren

    def get_sender_message(self, message, sender):
        pass