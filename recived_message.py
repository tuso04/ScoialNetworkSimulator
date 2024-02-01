import message


class Recived_Message(message.Message):

    def __init__(self, m, sender, time):
        super().__init__(m.message_id,
                         m.mood,
                         m.argumentative_quality,
                         m.emotional_dimension,
                         m.start_time,
                         m.life_time)
        self.message = m
        self.sender = sender
        self.time = time


