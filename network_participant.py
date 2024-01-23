import random

import message_stack
import recived_message

# Externe Bibliotheken
from scipy.stats import logistic

import relationship


class Network_Participant:
    def __init__(self, np_id, threshold_belive_p, turbulence_factor, indifference, isi_parameter, fi_parameter,
                 purchase_prob,
                 neighbors=None):
        if neighbors is None:
            neighbors = {}

        self.np_id = np_id  # id zur Identifikation, int
        # self.network = network                              # Netzwerk, zu dem der Knoten gehört, Network()
        self.threshold_belive_p = threshold_belive_p  # Schwellenwert für positive Nachrichten, double
        self.turbulence_factor = turbulence_factor
        self.indifference = indifference  # Spanne der Gleichgültigkeit double [0; 1]
        self.isi_parameter = isi_parameter  # Ausgleichsparameter bei Berechnung ISI double [0; 1]
        self.fi_parameter = fi_parameter  # Ausgleichsparameter bei Weiterleitungsabsicht double [0; 1]
        self.purchase_prob = purchase_prob  # initiale Kaufwahrscheinlichkeit, double
        self.neighbors = neighbors  # Nachbarn, Liste mit Relationship-Objekten
        self.recieve_box = message_stack.Message_Stack()  # Eingangsstapel, Message_stack
        self.send_box = message_stack.Message_Stack()  # Ausgangsstapel, Message_stack

    # Nachrichten Eingang

    def send(self, message, reciver, time):
        #print(f"{reciver.np_id} in {self.neighbors.keys()}")
        if reciver.np_id in self.neighbors.keys():
            reciver.recive(message, self, time)

    def recive(self, message, sender, time):
        self.recieve_box.add(
            recived_message.Recived_Message(message, sender, time), sender)  # Umwandlung in ein Recived_message Objekt

    # *****************************************Glauben****************************************************************

    # Glaubwürdigkeit (Cm/it)
    def credibility(self, message, time):
        credibility = (self.turbulence_factor * self.nsi(message, time) +
                       (1 - self.turbulence_factor) * self.isi(message))
        return credibility

    # Glauben   Option einbauen, wenn keine Konter Nachricht verfügbar!!!
    def believe(self, message, conter_message, time):
        if ((self.credibility(message, time) >= self._threshold_believe(message)) and
                (self.credibility(conter_message, time) <= self._threshold_believe(conter_message))):
            return True

        if (self.credibility(message, time) >= self._threshold_believe(message)
            and self.credibility(conter_message, time) >= self._threshold_believe(conter_message)) \
                and self._threshold_ex(message, time) > self._threshold_ex(conter_message, time) \
                and abs(
            self._threshold_ex(message, time) - self._threshold_ex(conter_message, time) >= self.indifference):
            return True

        return False

    # Schwellenwert Glauben → negative Nachrichten werden eher geglaubt werden
    def _threshold_believe(self, message):
        if not message:
            return 0

        if not message.mood:
            return self.threshold_belive_p / 2
        return self.threshold_belive_p

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

        for r in self.recieve_box.messages:
            if r.time == time and message.message_id == r.message_id:  # Muss noch in Message Klasse implementiert werden
                realtionship_pressure = self.neighbors.get(r.sender.np_id).bond
                pressure += realtionship_pressure

        social_pressure = pressure / self._compute_social_bond()

        return logistic.cdf(social_pressure)

    # Informatial social influence
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

    # Weiterleitungswahrscheinlichkeit      Option einbauen, wenn keine Konter Nachticht verfügbar!!!
    def forwarding_prob(self, message, conter_message, time):
        if conter_message is not None:
            if message.aging_factor >= conter_message.aging_factor:
                return self.forwarding_intent(message, time) * conter_message.aging_factor

        return self.forwarding_intent(message, time) * message.aging_factor

    # Weiterleitungsentscheidung    Option einbauen, wenn keine Konter Nachticht verfügbar!!!
    def forwarding_decision(self, message, conter_message, time, target):
        if (self.forwarding_prob(message, conter_message, time) >= random.randrange(0, 100) / 100) \
                and not self.send_box.get_sender_message(message, target) \
                and self.believe(message, conter_message, time):
            return True

        return False

    # ****************************************Kaufabsicht**************************************************************
    # Kaufabsicht       Option einbauen, wenn keine Konter Nachricht verfügbar!!!
    def purchase_int(self, message, conter_message, time):
        if self.believe(message, conter_message, time):
            # return self.purchase_prob +  *(1-math.e**(*self.credibility(message, conter_message,time)))
            pass

        if self.believe(conter_message, message, time):
            # return self.purchase_prob -
            pass

        return self.purchase_prob

    # Kaufentscheidung      Option einbauen, wenn keine Konter Nachticht verfügbar!!!
    def purchase_decision(self, message, conter_message, time):
        if self.purchase_int(message, conter_message, time) >= random.randrange(0, 100) / 100:
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
        conter_messages = {}  # alle Nachrichten mit negativem Mood in dict id - message
        for rm in self.recieve_box.messages:
            if rm.time == time:
                if rm.mood:
                    messages[rm.message_id] = rm
                else:
                    conter_messages[rm.message_id] = rm

                # Über alle positiven Nachrichten iterieren und verarbeiten
                for m in messages.values():

                    # Nach passender Konter nachricht suchen
                    cm = None
                    if m.message_id in conter_messages.keys():
                        cm = conter_messages.get(m.message_id)

                    # Algorithmen zu Glauben, Kaufverhalten und Weiterleitung
                    forward = {}
                    belive = self.believe(m, cm, time)
                    for n in self.neighbors.keys():
                        forward[n] = self.forwarding_decision(m, cm, time, n)
                    purchase = self.purchase_decision(m, cm, time)
                    print(f"m: {m.message_id}, belive: {belive}, purchase: {purchase}, forward: {forward}")

