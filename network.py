import random

import networkx as nx
import pickle

import pandas as pd

import bot
import message
import network_participant
import recived_message


class Network:
    def __init__(self, graph_json,
                 turbulence_factor,
                 n_influencer,
                 n_bots,
                 message_params,
                 counter_message_params,
                 relationships=None, participants=None):
        if participants is None:
            participants = {}
        if relationships is None:
            relationships = {}

        self.graph_json = graph_json  # NetworkX Graph in JSON verpackt
        self.graph = nx.adjacency_graph(self.graph_json)  # NetworkX Graph
        self.turbulence_factor = turbulence_factor  # Turbulenz des Marktes
        self.n_influencer = n_influencer  # Anzahl der Influencer
        self.n_bots = n_bots  # Anzahl der Bots
        self.message_params = message_params  # Parameter für die Nachricht
        self.counter_message_params = counter_message_params  # Parameter für die Gegennachricht
        self.relationships = relationships  # Beziehungen
        self.participants = participants  # Teilnehmer
        self.simulation_data = pd.DataFrame()  # DataFrame in dem die Auswertungsdaten gespeichert werden

        self.bots = []  # Liste mit Bots
        self.influencer = []  # Liste mit Influencern

    # Funktion zum Erzeugen von Influencern
    def _create_influencer(self):

        influencer = []

        # Grad jedes Knotens ermitteln
        degrees = dict(self.graph.degree())

        # Dictionary nach Werten sortieren
        sorted_dict = dict(sorted(degrees.items(), key=lambda item: item[1], reverse=True))

        # Die ersten x Elemente ausgeben
        count = 0
        for key, value in sorted_dict.items():
            if count == self.n_influencer:
                break
            if key != 0:
                influencer.append(key)
                count += 1

        return influencer

    # Funktion zum Erzeugen von Bots
    def _create_bots(self):
        bots = []

        for i in range(self.n_bots):
            b = random.randint(0, len(self.graph.nodes) - 1)
            while b in bots or b in self.influencer or b == 0:
                b = random.randint(0, len(self.graph.nodes) - 1)
            bots.append(b)

        return bots

    # Aus networkX Graph Objekte der Klasse Network_participant erzeugen
    def create_objects_from_graph(self):

        # Listen mit Knoten und Kanten
        nodes = self.graph.nodes
        edges = self.graph.edges

        # Bots
        self.influencer = self._create_influencer()
        self.bots = self._create_bots()

        # Erzeugung Network-Participant-Objekte aus NetworkX-Graph
        for i in range(len(nodes)):
            if i in self.bots:
                new_n_p = bot.Bot(
                    np_id=nodes[i]["np_id"],
                    threshold_believe_p=nodes[i]["threshold_believe_p"],
                    threshold_believe_n=nodes[i]["threshold_believe_n"],
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
                    threshold_believe_p=nodes[i]["threshold_believe_p"],
                    threshold_believe_n=nodes[i]["threshold_believe_n"],
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

            # Füllen des Dictionary mit Teilnehmern: "<Teilnehmer-ID>": "<Netzwerkteilnehmer-Objekt>"
            self.participants[new_n_p.np_id] = new_n_p

        # Erzeugung Relationship-Objekte aus NetworkX Graph (0, 3)
        for e in edges:
            self.relationships[e] = self.participants.get(e[0]).add_neighbor(
                neighbor=self.participants.get(e[1]),
                bond=self.graph[e[0]][e[1]]["bond"][0])
            self.relationships[(e[1], e[0])] = self.participants.get(e[1]).add_neighbor(
                neighbor=self.participants.get(e[0]),
                bond=self.graph[e[0]][e[1]]["bond"][1])

    """def update_graph(self):
        # Listen mit Knoten und Kanten
        nodes = self.graph.nodes

        for i in range(len(nodes)):
            n_p = self.participants.get(nodes[i]["np_id"])
            nodes[i]["send_box"] = pickle.dumps(n_p.send_box).decode('latin1')
            nodes[i]["get_message"] = n_p.n_message
            nodes[i]["get_conter_message"] = n_p.n_conter_message
            nodes[i]["believe"] = False
            nodes[i]["forwarding"] = False
            nodes[i]["purchase"] = False"""

    def simulate_network(self, time):
        global prob_forward, prob_counter_forward
        print(f"**************************New Step {time}***************************")

        # Initiale Nachrichten
        if time == self.message_params["start_time"] and self.message_params["check"]:
            start_points = []

            # Influencer werden als Startpunkte hinzugefügt
            for i in self.influencer:
                start_points.append(self.participants.get(i))

            # Knoten 0 als Unternehmen zu Startpunkten hinzugefügt
            company = self.participants.get(0)
            start_points.append(company)

            # Nachricht wird erschaffen
            m = message.Message(1,
                                True,
                                self.message_params["quality"],
                                self.message_params["emotionality"],
                                time,
                                self.message_params["life_time"])

            # Nachbarn der Startpunkte ermittelt
            for starter in start_points:
                first_customer = starter.neighbors.values()

                for c in first_customer:
                    packed_m = recived_message.Recived_Message(m, c.part_B, time-1)
                    starter.send_box.add(packed_m, c.part_B)
                    print(f"{starter.np_id} sendet an {c.part_B.np_id} Nachricht {m.message_id} zu {time-1}")

        # Initiale Gegennachricht
        if time == self.counter_message_params["start_time"] and self.counter_message_params["check"]:
            counter_message_startpoint = random.randint(1, len(self.graph.nodes) - 1)

            while counter_message_startpoint in self.influencer or counter_message_startpoint in self.bots:
                counter_message_startpoint = random.randint(1, len(self.graph.nodes) - 1)

            counter_message_startpoint_participant = self.participants.get(counter_message_startpoint)

            cm = message.Message(2,
                                 False,
                                 self.counter_message_params["quality"],
                                 self.counter_message_params["emotionality"],
                                 time,
                                 self.counter_message_params["life_time"])

            first_cm_receiver = counter_message_startpoint_participant.neighbors.values()

            for c in first_cm_receiver:
                packed_cm = recived_message.Recived_Message(cm, c.part_B, time - 1)
                counter_message_startpoint_participant.send_box.add(packed_cm, c.part_B)
                print(
                    f"{counter_message_startpoint_participant.np_id} sendet an {c.part_B.np_id} Nachricht {cm.message_id}")

        # Sende alle Nachrichten im Netzwerk
        for np in list(self.participants.values()):
            for neighbor in np.send_box.messages_by_sender.keys():

                packed_m2 = np.send_box.messages_by_sender.get(neighbor)

                if packed_m2.time == time - 1:
                    np.send(message=packed_m2.message,
                            receiver=neighbor,
                            time=time)

        # Verarbeite die empfangenen Nachrichten jedes Kontos
        for np in self.participants.values():
            np.process_messages(time)

        # Datenzusammenfassung pro Step
        spreading = 0
        counter_spreading = 0
        net_believe = 0
        net_counter_believe = 0
        sum_net_credibility = 0
        sum_net_counter_credibility = 0
        net_forward = 0
        net_counter_forward = 0
        net_purchase = 0
        sum_purchase = 0

        for np in self.participants.values():
            if np.n_message > 0:
                spreading += 1
            if np.n_counter_message > 0:
                counter_spreading += 1
            if np.m_believe:
                net_believe += 1
            if np.cm_believe:
                net_counter_believe += 1
            sum_net_credibility += np.m_credibility
            sum_net_counter_credibility += np.cm_credibility
            if np.m_forwarding:
                net_forward += 1
            if np.cm_forwarding:
                net_counter_forward += 1
            if np.purchase:
                net_purchase += 1
            sum_purchase += np.purchase_intent

            prob_forward = 0
            if spreading > 0:
                prob_forward = net_forward / spreading

            prob_counter_forward = 0
            if counter_spreading > 0:
                prob_counter_forward = net_counter_forward / counter_spreading

        step_data_network = {
            "prob_spreading": spreading / len(self.participants),
            "prob_counter_spreading": counter_spreading / len(self.participants),
            "avg_credibility": sum_net_credibility / len(self.participants),
            "avg_counter_credibility": sum_net_counter_credibility / len(self.participants),
            "prob_believe": net_believe / len(self.participants),
            "prob_counter_believe": net_counter_believe / len(self.participants),
            "prob_forward": prob_forward,
            "prob_counter_forward": prob_counter_forward,
            "prob_purchase": net_purchase / len(self.participants),
            "avg_purchase": sum_purchase / len(self.participants),
        }

        print(step_data_network)

        self.simulation_data = pd.concat([self.simulation_data, pd.DataFrame(step_data_network, index=[time])],
                                         ignore_index=True)
