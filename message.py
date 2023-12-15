class Message:

    def __init__(self, message_id, mood, argumentative_quality, emotional_dimension):
        self.message_id = message_id                           # Zahl
        self.mood = mood                                       # boolean
        self.argumentative_quality = argumentative_quality     # double zwischen 0 und 1
        self.emotional_dimension = emotional_dimension         # double zwischen 0 und 1