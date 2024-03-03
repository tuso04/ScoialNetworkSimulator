import math


class Message:

    def __init__(self, message_id, mood, argumentative_quality, emotional_dimension, start_time, life_time):
        self.message_id = message_id  # Zahl
        self.mood = mood  # boolean
        self.argumentative_quality = argumentative_quality  # double zwischen 0 und 1
        self.emotional_dimension = emotional_dimension  # double zwischen 0 und 1
        self.start_time = start_time
        self.life_time = life_time
        self.aging_factor = self.compute_aging_factor(start_time)

    def compute_aging_factor(self, time):
        self.aging_factor = math.exp(-math.log(2) * ((self.life_time / 2) ** (-1)) * (time - self.start_time))
        #print(f"{self.aging_factor} = exp({-math.log(2)}* ({self.life_time}/2 ** (-1) * ({time} - {self.start_time}")
        return self.aging_factor
