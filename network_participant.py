import random

import message_stack
import recived_message

# Externe Bibiliotheken
from scipy.stats import logistic


class Network_Participant:
    def __init__(self, np_id, network, threshold_belive_p, indifference, isi_parameter, fi_parameter, purchase_prob, neighbor):
        self.np_id = np_id                                  # id zur Identifikation, int
        self.network = network                              # Netzwerk, zu dem der Knoten gehört, Network()
        self.threshold_belive_p = threshold_belive_p        # Schwellenwert für positive Nachrichten, double
        self.indifference = indifference                    # Spanne der Gleichgültigkeit double [0; 1]
        self.isi_parameter = isi_parameter                  # Ausgleichsparameter bei Berechnung ISI double [0;1]
        self.fi_parameter = fi_parameter                    # Ausgleichsparameter bei Weiterleitungsabsicht double [0;1]
        self.purchase_prob = purchase_prob                  # initiale Kaufwahrscheinlichkeit, double
        self.neighbor = neighbor                            # Nachbarn, Liste mit Relationship-Objekten
        self.recieve_box = message_stack.Message_Stack()    # Eingangsstapel, Message_stack
        self.send_box = message_stack.Message_Stack()       # Ausgangsstapel, Message_stack

    # Nachrichten Eingang
    def recive(self, message, sender, time):
        self.recieve_box.add(
            recived_message.Recived_Message(message, sender, time))  # Umwandlung in ein Recived_message Objekt

    # *****************************************Glauben****************************************************************

    # Glaubwürdigkeit (Cm/it)
    def credibility(self, message, time):
        credibility = (self.network.turbulence_factor * self.nsi(message, time) +
                       (1 - self.network.turbulence_factor) * self.isi(message))
        return credibility

    # Glauben
    def belive(self, message, conter_message, time):
        if ((self.credibility(message, time) >= self._threshold_belive(message)) and
                (self.credibility(conter_message, time) <= self._threshold_belive(conter_message))):
            return True

        if (self.credibility(message, time) >= self._threshold_belive(message)
                and self.credibility(conter_message, time) >= self._threshold_belive(conter_message))\
                and self._threshold_ex(message, time) > self._threshold_ex(conter_message, time)\
                and abs(self._threshold_ex(message, time)-self._threshold_ex(conter_message, time) >= self.indifference):
            return True

        return False

    # Schwellenwert Glauben -> negative Nachrichten werden eher geglaubt werden
    def _threshold_belive(self, message):
        if not message.mood:
            return self.threshold_belive_p / 2
        return self.threshold_belive_p

    def _threshold_ex(self, message, time):
        if self.credibility(message, time) >= self._threshold_belive(message):
            return (self.credibility(message, time)-self._threshold_belive(message))/(1-self._threshold_belive(message))
        return self.credibility(message, time)

    # Normative social influence
    def nsi(self, message, time):
        pressure = 0

        for r in self.recieve_box.messages:
            if r.time == time and message == r.message:  # Muss noch in Message Klasse implementiert werden
                realtionship_pressure = self.neighbor.get(r.sender).bond
                pressure += realtionship_pressure

        social_pressure = pressure / self._compute_social_bond()

        return logistic.cdf(social_pressure)

    # Informatial social influence
    def isi(self, message):
        return self.isi_parameter*message.argumentative_quality + (1 - self.isi_parameter)*message.emotional_dimension

    # *****************************************Weiterleiten************************************************************

    # Weitleitungsabsicht
    def forwarding_intent(self, message, time):
        b = self.neighbor.get(message.sender).bond

        return (self.fi_parameter*b*self.credibility(message, time)
                + (1-self.fi_parameter))*(b+self.credibility(message, time)-b*self.credibility(message, time))

    # Weiterleitungswahrscheinlichkeit
    def forwarding_prob(self, message, conter_message, time):
        if conter_message is not None:
            if message.aging_factor >= conter_message.aging_factor:
                return self.forwarding_intent(message, time) * conter_message.aging_factor

        return self.forwarding_intent(message, time) * message.aging_factor

    # Weiterleitungsentscheidung
    def forwarding_decision(self, message, conter_message, time, target):
        if (self.forwarding_prob(message, conter_message, time) >= random.randrange(0, 100)/100) \
                and not self.send_box.get_sender_message(message, target) \
                and self.belive(message, conter_message, time):
            return True

        return False

    # ****************************************Hilfsfunktionen**********************************************************

    # Hilfsfunkiton Berechnung Soziale Bindung
    def _compute_social_bond(self):
        social_bond = 0

        for np in self.neighbor.keys():
            social_bond += self.neighbor.get(np).bond

        return social_bond
