import networkx as nx
import pickle

import message
import message_stack
import network_participant
import recived_message
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
                purchase_prob=nodes[i]["purchase_prob"],
                send_box=(pickle.loads(nodes[i]["send_box"].encode('latin1')) if nodes[i]["send_box"] else None)
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

    def update_graph(self):
        # Listen mit Knoten und Kanten
        nodes = self.graph.nodes

        for i in range(len(nodes)):
            n_p = self.participants.get(nodes[i]["np_id"])
            nodes[i]["send_box"] = pickle.dumps(n_p.send_box).decode('latin1')
            nodes[i]["get_message"] = n_p.n_message
            nodes[i]["get_conter_message"] = n_p.n_conter_message
            nodes[i]["believe"] = False
            nodes[i]["forwarding"] = False
            nodes[i]["purchase"] = False

    def simulate_network(self, time):
        print(f"**************************New Step {time}***************************")

        if time == 0:
            company = self.participants.get(0)
            first_customer = company.neighbors.values()
            m = message.Message(1,
                                True,
                                0.5,
                                0.5,
                                time,
                                5)

            for c in first_customer:
                packed_m = recived_message.Recived_Message(m, c.part_B, -1)
                company.send_box.add(packed_m, c.part_B)

        # Sende alle Nachrichten im Netzwerk
        for np in list(self.participants.values()):
            # print(f"{np.np_id} {np.}")
            for neighbor in np.send_box.messages_by_sender.keys():

                #print(f"Message Type: {type(np.send_box.messages_by_sender.get(neighbor))}")
                packed_m2 = np.send_box.messages_by_sender.get(neighbor)

                if packed_m2.time == time - 1:
                    np.send(message=packed_m2.message,
                            reciver=neighbor,
                            time=time)
                    #for np2 in self.participants.values():
                        #print(f"Nach dem Senden: {np2.np_id} zu {time}: {np2.recieve_box.messages_by_sender} ")

        # Verarbeite die empfangenen Nachrichten jedes Konten
        for np in self.participants.values():
            #print(f"Vor: {np.np_id} zu {time}: {np.recieve_box.messages_by_sender} ")
            np.process_messages(time)

        #self.update_graph()
