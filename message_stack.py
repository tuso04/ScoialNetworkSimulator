class Message_Stack:
    def __init__(self):
        self.messages = []
        self.messages_by_sender = {}

    def add(self, message, network_participant):
        self.messages.append(message)
        self.messages_by_sender[network_participant] = message

    def get_sender_message(self, message, sender):
        for s in self.messages_by_sender:
            if message == self.messages_by_sender.get(s) and sender == s:
                return True
        return False
