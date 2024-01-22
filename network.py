import networkx as nx

import message
import network_participant
import relationship


class Network:
    def __init__(self, graph_json, turbulence_factor, relationships=None, participants=None):
        if participants is None:
            participants = {}
        if relationships is None:
            relationships = {}

        self.graph_json = graph_json
        self.graph = nx.adjacency_graph(self.graph_json)
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
        part_A.neighbors[part_B] = rel
        part_B.neighbors[part_A] = rel

    def create_objects_from_graph(self):

        # Listen mit Knoten und Kanten
        nodes = self.graph.nodes
        edges = self.graph.edges

        # Erzeugung Network-Participant-Objekte aus json
        for i in range(len(nodes)):
            new_n_p = network_participant.Network_Participant(
                np_id=nodes[i]["np_id"],
                threshold_belive_p=nodes[i]["threshold_belive_p"],
                turbulence_factor=nodes[i]["turbulence_factor"],
                indifference=nodes[i]["indifference"],
                isi_parameter=nodes[i]["isi_parameter"],
                fi_parameter=nodes[i]["fi_parameter"],
                purchase_prob=nodes[i]["purchase_prob"]
            )

            self.participants[new_n_p.np_id] = new_n_p

        # Erzeugung Relationship-Objekte aus json
        for e in edges:
            self.relationships[e] = self.participants.get(e[0]).add_neighbor(
                neighbor=self.participants.get(e[1]),
                bond=self.graph[e[0]][e[1]]["bond"][0])
            self.relationships[(e[1], e[0])] = self.participants.get(e[1]).add_neighbor(
                neighbor=self.participants.get(e[0]),
                bond=self.graph[e[0]][e[1]]["bond"][1])

    def simulate_network(self, time):
        company = self.participants.get(0)
        first_customer = company.neighbors.values()
        m = message.Message(1,
                            True,
                            0.5,
                            0.5,
                            time,
                            5)
        for c in first_customer:
            print(c)
            company.send_box.add(m, c.part_B)



        # Sende alle Nachrichten im Netzwerk
        for np in self.participants.values():
            for m in np.send_box.messages_by_sender.keys():
                np.send(message=np.send_box.messages_by_sender.get(m),
                        reciver=m,
                        time=time)

        # Verarbeite die empfangenen Nachrichten jedes Konten
        for np in self.participants.values():
            np.process_messages(time)
