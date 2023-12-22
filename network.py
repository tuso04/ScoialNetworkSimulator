import relationship


class Network:
    def __init__(self, turbulence_factor, relationships=None, participants=None):
        if participants is None:
            participants = []
        if relationships is None:
            relationships = []
        self.turbulence_factor = turbulence_factor
        self.relationships = relationships
        self.participants = participants

    def add_participant(self, participant):
        self.participants.append(participant)

    def add_participants(self, participants):
        for p in participants:
            self.participants.append(p)

    def add_relationship(self, part_A, part_B, bond):
        rel = relationship.Relationship(part_A, part_B, bond)
        self.relationships.append(rel)
        part_A.neighbor[part_B] = rel
        part_B.neighbor[part_A] = rel
