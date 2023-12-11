
import message_stack

### Externe Bibiliotheken
from scipy.stats import logistic


class Network_Participant:
    def __init__(self, network, threshold_belive_p, neighbor):
        self.network = network                              # Netzwerk, zu dem der Knoten gehört
        self.threshold_belive_p = threshold_belive_p        # Schwellenwert für positive Nachrichten
        self.neighbor = {}                           # Liste mit Relationship-Objekten
        self.recieve_box = message_stack.Message_stack()

        self._social_bond = self._compute_social_bond()


    ## Glaubwürdigkeit (Cm/it)
    def credibility(self, message, time):
        credibility = (self.network.get_turbulence_factor * self.nsi(message, time) +
                       (1 - self.network.get_turbulence_factor) * self.isi(message, time))
        return credibility

    ## Glauben
    def belive(self,message, conter_message, time):
        threshold_ex_message = self._threshold_ex_belive(message, time)
        threshold_ex_conter_message = self._threshold_ex_belive(conter_message, time)

        if (self.credibility(message,time) >= self._threshold_belive(message)) and (self.credibility(conter_message) <= self._threshold_belive(conter_message)):
            return True

        ######## Logik noch zu überarbeiten
        if self.credibility(message, time) >= self._threshold_belive(message) and self.credibility(
                conter_message) >= self._threshold_belive(conter_message):
            pass
        return False


    ## Schwellenwert Glauben -> negative Nachrichten werden eher geglaubt werden
    def _threshold_belive(self, message):
        if not message.mood:
            return self.threshold_belive_p/2
        return self.threshold_belive_p

    ## Schwellwertüberschreitung Glauben
    def _threshold_ex_belive(self, message, time):
        return ((self.credibility(message, time) - self._threshold_belive) /
                (1 - self._threshold_belive))

    ## Hilfsfunkiton Berechnung Soziale Bindung
    def _compute_social_bond(self):
        social_bond = 0

        for np in self.neighbor.keys():
            social_bond += self.neighbor.get(np).bond

        return social_bond

    ## Normative social influence
    def nsi(self, message, time):
        pressure = 0

        for r in self.recieve_box.messages:
            if r.time == time and message == r.message:     ### Muss noch in Message Klasse implementiert werden
                realtionship_pressure = self.neighbor.get(r.sender).bond
                pressure += realtionship_pressure

        social_pressure = pressure/self._social_bond

        return logistic.cdf(social_pressure)


    def isi(self, message):
