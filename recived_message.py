import message


class Recived_Message(message.Message):

    def __init__(self, message, sender, time):
        super().__init__(id, message.mood, message.argumentative_quality, message.emotional_dimension)
        self.sender = sender
        self.time = time
