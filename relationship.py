import random


class Relationship:
    def __init__(self, part_A, part_B, bond):
        self.part_A = part_A
        self.part_B = part_B
        self.bond = bond
        self.u = random.randint(0, 100) / 100
