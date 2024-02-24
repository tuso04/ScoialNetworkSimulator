import math
import random

import message_stack
import recived_message

# Externe Bibliotheken
from scipy.special import expit

import relationship


class Network_Participant:
    def __init__(self, np_id, threshold_believe_p, turbulence_factor, indifference, isi_parameter, fi_parameter,
                 purchase_init_prob, purchase_prob_max, purchase_prob_min, purchase_expo_param_positive,
                 purchase_expo_param_negative,
                 neighbors=None, send_box=None):
        if neighbors is None:
            neighbors = {}
        if send_box is None:
            send_box = message_stack.Message_Stack()

        self.np_id = np_id  # id zur Identifikation, int
        # self.network = network # Netzwerk, zu dem der Knoten gehört, Network()
        self.threshold_believe_p = threshold_believe_p  # Schwellenwert für positive Nachrichten, double
        self.turbulence_factor = turbulence_factor
        self.indifference = indifference  # Spanne der Gleichgültigkeit double [0; 1]
        self.isi_parameter = isi_parameter  # Ausgleichsparameter bei Berechnung ISI double [0; 1]
        self.fi_parameter = fi_parameter  # Ausgleichsparameter bei Weiterleitungsabsicht double [0; 1]
        self.purchase_init_prob = purchase_init_prob  # initiale Kaufwahrscheinlichkeit, double
        self.purchase_prob = purchase_init_prob  # Kaufwahrscheinlichkeit
        self.purchase_prob_max = purchase_prob_max  # Obere Grenze Berechnung Kaufwahrscheinlichkeit
        self.purchase_prob_min = purchase_prob_min  # Untere Grenze Berechnung Kaufwahrscheinlichkeit
        self.purchase_expo_param_positive = purchase_expo_param_positive  # Exponential Faktor Kaufwahrscheinlichkeit positiv
        self.purchase_expo_param_negative = purchase_expo_param_negative  # Exponential Faktor Kaufwahrscheinlichkeit negativ
        self.neighbors = neighbors  # Nachbarn, Liste mit Relationship-Objekten
        self.centrality_degree = len(self.neighbors)
        self.receive_box = message_stack.Message_Stack()  # Eingangsstapel, Message_stack
        self.send_box = send_box  # Ausgangsstapel, Message_stack

        # Anzeigeparameter der Knoten
        self.n_message = 0
        self.n_counter_message = 0
        self.m_believe = False
        self.cm_believe = False
        self.m_credibility = 0
        self.cm_credibility = 0
        self.m_forwarding = False
        self.cm_forwarding = False
        self.n_m_forwarding = 0
        self.prob_forwarding = 0
        self.m_purchase = False

    # Nachrichten Eingang

    def send(self, message, receiver, time):
        if receiver.np_id in self.neighbors.keys():
            # print(f"{self.np_id} an {receiver.np_id} zu {time}")
            receiver.receive_box.add(recived_message.Recived_Message(message, self, time), self)
            # receiver.receive(message, self, time)

    """def receive(self, message, sender, time):
        print(f"{self.np_id} bekommt von {sender.np_id} zu {time}")
        self.recieve_box.add(
            recived_message.Recived_Message(message, sender, time), sender)  # Umwandlung in ein Recived_message Objekt
        print(f"{self.np_id} {self.recieve_box.messages_by_sender}")"""

    # *****************************************Glauben****************************************************************

    # Glaubwürdigkeit (Cm/it)
    def credibility(self, message, time):
        credibility = (self.turbulence_factor * self.nsi(message, time) +
                       (1 - self.turbulence_factor) * self.isi(message))
        return credibility

    # Glauben   Option einbauen, wenn keine Konter Nachricht verfügbar!!!
    def believe(self, message, counter_message, time):
        if ((self.credibility(message, time) >= self._threshold_believe(message)) and
                (self.credibility(counter_message, time) <= self._threshold_believe(counter_message))):
            return True

        if (self.credibility(message, time) >= self._threshold_believe(message)
            and self.credibility(counter_message, time) >= self._threshold_believe(counter_message)) \
                and self._threshold_ex(message, time) > self._threshold_ex(counter_message, time) \
                and abs(
            self._threshold_ex(message, time) - self._threshold_ex(counter_message, time) >= self.indifference):
            self.m_believe = True
            return True

        return False

    # Schwellenwert Glauben → negative Nachrichten werden eher geglaubt werden
    def _threshold_believe(self, message):
        if not message:
            return 0

        if not message.mood:
            return self.threshold_believe_p / 2
        return self.threshold_believe_p

    def _threshold_ex(self, message, time):
        if self.credibility(message, time) >= self._threshold_believe(message):
            return (self.credibility(message, time) - self._threshold_believe(message)) / (
                    1 - self._threshold_believe(message))
        return self.credibility(message, time)

    # Normative social influence
    def nsi(self, message, time):
        if not message:
            return 0

        pressure = 0
        slope = 0.25
        intercept = 20

        for r in self.receive_box.messages:
            if r.time == time and message.message_id == r.message_id:  # Muss noch in Message Klasse implementiert werden
                relationship_pressure = self.neighbors.get(r.sender.np_id).bond
                pressure += relationship_pressure

        social_pressure = pressure / self._compute_social_bond()
        x = slope * social_pressure + intercept

        return expit(x)

    # Information social influence
    def isi(self, message):
        if not message:
            return 0

        return self.isi_parameter * message.argumentative_quality + (
                1 - self.isi_parameter) * message.emotional_dimension

    # *****************************************Weiterleiten************************************************************

    # Weiterleitungsabsicht
    def forwarding_intent(self, message, time):
        if not message:
            return 0

        b = self.neighbors.get(message.sender.np_id).bond

        return (self.fi_parameter * b * self.credibility(message, time)
                + (1 - self.fi_parameter)) * (b + self.credibility(message, time) - b * self.credibility(message, time))

    # Weiterleitungswahrscheinlichkeit
    def forwarding_prob(self, message, counter_message, time):
        if counter_message is not None:
            if message.aging_factor >= counter_message.aging_factor:
                return self.forwarding_intent(message, time) * counter_message.aging_factor

        return self.forwarding_intent(message, time) * message.aging_factor

    # Weiterleitungsentscheidung
    def forwarding_decision(self, message, counter_message, time, target):
        if (self.forwarding_prob(message, counter_message, time) >= random.randrange(0, 100) / 100) \
                and not self.send_box.get_sender_message(message, target) \
                and self.believe(message, counter_message, time):
            if message.mood:
                self.m_forwarding = True
            else:
                self.cm_forwarding = True

            return True
        return False

    # ****************************************Kaufabsicht**************************************************************
    # Kaufabsicht       Option einbauen, wenn keine Konter Nachricht verfügbar!!!
    def purchase_int(self, message, counter_message, time):
        if self.believe(message, counter_message, time):
            return self.purchase_prob + (self.purchase_prob_max - self.purchase_prob) * (
                    1 - math.e ** (self.purchase_expo_param_positive * self.credibility(message, time)))

        if self.believe(counter_message, message, time):
            return self.purchase_prob + (self.purchase_prob - self.purchase_prob_min) * (
                    1 - math.e ** (self.purchase_expo_param_negative * self.credibility(message, time)))

        return self.purchase_prob

    # Kaufentscheidung
    def purchase_decision(self, message, counter_message, time):
        if self.purchase_int(message, counter_message, time) >= random.randrange(0, 100) / 100:
            self.m_purchase = True
            return True
        return False

    # ****************************************Hilfsfunktionen**********************************************************

    # Hilfsfunktion Berechnung soziale Bindung
    def _compute_social_bond(self):
        social_bond = 0

        for np in self.neighbors.keys():
            social_bond += self.neighbors.get(np).bond

        return social_bond

    # Füge Nachbarn hinzu
    def add_neighbor(self, neighbor, bond):
        rel = relationship.Relationship(self, neighbor, bond)

        self.neighbors[neighbor.np_id] = rel

        return rel

    # Verarbeitung der Nachrichten nach Glauben, Weiterleitung, Kaufverhalten
    def process_messages(self, time):
        messages = {}  # alle Nachrichten mit positivem Mood in dict id - message
        counter_messages = {}  # alle Nachrichten mit negativem Mood in dict id - message

        # Anzeige Parameter zurücksetzen
        self.m_believe = False
        self.m_forwarding = False
        self.m_purchase = False

        # print(f"{self.np_id} zu {time}: {self.receive_box.messages_by_sender} ")
        for rm in self.receive_box.messages:
            if rm.time == time:
                if rm.mood:
                    messages[rm.message_id] = rm
                    self.n_message += 1
                else:
                    counter_messages[rm.message_id] = rm
                    self.n_counter_message += 1

                # Über alle positiven Nachrichten iterieren und verarbeiten
                for m in messages.values():

                    # Nach passender Konter nachricht suchen
                    cm = None

                    # Auslegung auf nur eine Nachricht und eine Gegennachricht
                    if m.message_id + 1 in counter_messages.keys():
                        cm = counter_messages.get(m.message_id + 1)

                    # Algorithmen zu Glauben, Kaufverhalten und Weiterleitung
                    forward = {}
                    self.m_credibility = self.credibility(m, time)
                    believe = self.believe(m, cm, time)
                    self.m_believe = believe
                    for n in self.neighbors.keys():
                        forward[n] = self.forwarding_decision(m, cm, time, n)
                    purchase = self.purchase_decision(m, cm, time)

                    for nb_id, f_decision in forward.items():
                        if f_decision:
                            self.send_box.add(m, self.neighbors.get(nb_id).part_B)

                    print(
                        f"id: {self.np_id} m: {m.message_id}, believe: {believe}, purchase: {purchase}, forward: {forward}")

                # Über alle positiven Nachrichten iterieren und verarbeiten
                for cm in counter_messages.values():

                    # Nach passender Konter nachricht suchen
                    m = None

                    # Auslegung auf nur eine Nachricht und eine Gegennachricht
                    if cm.message_id - 1 in messages.keys():
                        m = messages.get(cm.message_id - 1)

                    # Algorithmen zu Glauben, Kaufverhalten und Weiterleitung
                    forward = {}
                    self.cm_credibility = self.credibility(cm, time)
                    believe = self.believe(cm, m, time)
                    self.cm_believe = believe

                    for n in self.neighbors.keys():
                        if self.forwarding_decision(cm, m, time, n) is None:
                            print(f"{cm} - {m} - {self.forwarding_decision(cm, m, time, n)}")

                        forward[n] = self.forwarding_decision(cm, m, time, n)

                    for nb_id, f_decision in forward.items():
                        if f_decision:
                            self.send_box.add(cm, self.neighbors.get(nb_id).part_B)

                    print(
                        f"id: {self.np_id} m: {cm.message_id}, believe: {believe}, forward: {forward}")
