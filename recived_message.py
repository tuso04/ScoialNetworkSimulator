import message

class Recived_message(message.Message):

    def __init__(self, id, mood, argumentative_quality, emotional_dimension, sender, time):
        super().__init__(id, mood, argumentative_quality, emotional_dimension)
        self.sender = sender
        self.time = time