import random

import networkx as nx
import pickle

import pandas as pd

import bot
import message
import network_participant
import recived_message
import relationship


class Network:
    def __init__(self, graph_json, turbulence_factor, n_influencer, n_bots, message_start_time,
                 counter_message_start_time,
                 relationships=None, participants=None):
        if participants is None:
            participants = {}
        if relationships is None:
            relationships = {}

        self.graph_json = graph_json
        self.graph = nx.adjacency_graph(self.graph_json)
        self.turbulence_factor = turbulence_factor
        self.n_influencer = n_influencer
        self.n_bots = n_bots
        self.message_start_time = message_start_time
        self.counter_message_start_time = counter_message_start_time
        self.relationships = relationships
        self.participants = participants
        self.simulation_data = pd.DataFrame()

        self.bots = []
        self.influencer = []

    """def add_participant(self, participant):
        self.participants.append(participant)

    def add_participants(self, participants):
        for p in participants:
            self.participants.append(p)

    def add_relationship(self, part_A, part_B, bond):
        rel = relationship.Relationship(part_A, part_B, bond)
        self.relationships.append(rel)
        part_A.neighbors[part_B] = rel
        part_B.neighbors[part_A] = rel
        """

    def create_influencer(self):

        influencer = []

        # Grad jedes Knotens ermitteln
        degrees = dict(self.graph.degree())

        # Dictionary nach Werten sortieren
        sorted_dict = dict(sorted(degrees.items(), key=lambda item: item[1], reverse=True))

        # Die ersten x Elemente ausgeben
        count = 0
        for key, value in sorted_dict.items():
            if key != 0:
                influencer.append(key)
                count += 1
            if count == self.n_influencer:
                break

        return influencer

    def create_bots(self):
        bots = []

        for i in range(self.n_bots):
            b = random.randint(0, len(self.graph.nodes) - 1)
            while b in bots or b in self.influencer or b == 0:
                b = random.randint(0, len(self.graph.nodes) - 1)
            bots.append(b)

        return bots

    def create_objects_from_graph(self):

        # Listen mit Knoten und Kanten
        nodes = self.graph.nodes
        edges = self.graph.edges

        # Bots
        self.influencer = self.create_influencer()
        self.bots = self.create_bots()

        print(f"Influencer: {self.influencer}")
        print(f"Bots: {self.bots}")

        # Erzeugung Network-Participant-Objekte aus json
        for i in range(len(nodes)):
            if i in self.bots:
                new_n_p = bot.Bot(
                    np_id=nodes[i]["np_id"],
                    threshold_believe_p=nodes[i]["threshold_belive_p"],
                    turbulence_factor=nodes[i]["turbulence_factor"],
                    indifference=nodes[i]["indifference"],
                    isi_parameter=nodes[i]["isi_parameter"],
                    fi_parameter=nodes[i]["fi_parameter"],
                    purchase_init_prob=nodes[i]["purchase_prob"],
                    purchase_prob_max=nodes[i]["purchase_prob_max"],
                    purchase_prob_min=nodes[i]["purchase_prob_min"],
                    purchase_expo_param_negative=nodes[i]["purchase_prob_negative"],
                    purchase_expo_param_positive=nodes[i]["purchase_prob_positive"],
                    send_box=(pickle.loads(nodes[i]["send_box"].encode('latin1')) if nodes[i]["send_box"] else None)
                )
            else:
                new_n_p = network_participant.Network_Participant(
                    np_id=nodes[i]["np_id"],
                    threshold_believe_p=nodes[i]["threshold_belive_p"],
                    turbulence_factor=nodes[i]["turbulence_factor"],
                    indifference=nodes[i]["indifference"],
                    isi_parameter=nodes[i]["isi_parameter"],
                    fi_parameter=nodes[i]["fi_parameter"],
                    purchase_init_prob=nodes[i]["purchase_prob"],
                    purchase_prob_max=nodes[i]["purchase_prob_max"],
                    purchase_prob_min=nodes[i]["purchase_prob_min"],
                    purchase_expo_param_negative=nodes[i]["purchase_prob_negative"],
                    purchase_expo_param_positive=nodes[i]["purchase_prob_positive"],
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

        # Initiale Nachrichten
        if time == self.message_start_time:
            start_points = []

            for i in self.influencer:
                start_points.append(self.participants.get(i))

            company = self.participants.get(0)
            start_points.append(company)

            m = message.Message(1,
                                True,
                                0.5,
                                0.5,
                                time,
                                5)

            for starter in start_points:
                first_customer = starter.neighbors.values()

                for c in first_customer:
                    packed_m = recived_message.Recived_Message(m, c.part_B, -1)
                    starter.send_box.add(packed_m, c.part_B)
                    print(f"{starter.np_id} sendet an {c.part_B.np_id} Nachricht {m.message_id}")

        # Sende alle Nachrichten im Netzwerk
        for np in list(self.participants.values()):
            for neighbor in np.send_box.messages_by_sender.keys():

                packed_m2 = np.send_box.messages_by_sender.get(neighbor)

                if packed_m2.time == time - 1:
                    np.send(message=packed_m2.message,
                            reciver=neighbor,
                            time=time)

        # Verarbeite die empfangenen Nachrichten jedes Kontos
        for np in self.participants.values():
            np.process_messages(time)

        # Datenzusammenfassung pro Step
        spreading = 0
        net_believe = 0
        sum_net_credibility = 0
        net_forward = 0
        net_purchase = 0
        sum_purchase = 0

        for np in self.participants.values():
            if np.n_message > 0:
                spreading += 1
            if np.m_belive:
                net_believe += 1
            sum_net_credibility += np.m_credibility
            if np.m_forwarding:
                net_forward += 1
            if np.m_purchase:
                net_purchase += 1
            sum_purchase += np.purchase_prob

        step_data_network = {
            "prob_spreading": spreading / len(self.participants),
            "avg_credibility": sum_net_credibility / len(self.participants),
            "prob_believe": net_believe / len(self.participants),
            "prob_forward": net_forward / spreading,
            "prob_purchase": net_purchase / len(self.participants),
            "avg_purchase": sum_purchase / len(self.participants),
        }

        # print(pd.DataFrame(step_data_network, index=[time]))
        self.simulation_data = pd.concat([self.simulation_data, pd.DataFrame(step_data_network, index=[time])],
                                         ignore_index=True)

        # self.update_graph()
