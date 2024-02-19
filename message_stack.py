class Message_Stack:
    def __init__(self):
        self.messages = []
        self.messages_by_sender = {}

    def add(self, message, network_participant):
        self.messages.append(message)
        self.messages_by_sender[network_participant] = message

        ### add messages by sender noch implementieren

    def get_sender_message(self, message, sender):
        pass
