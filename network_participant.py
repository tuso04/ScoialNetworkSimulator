class Network_Participant:
    def __init__(self, network, threshold_belive_p, neighbor):
        self.network = network                              # Netzwerk, zu dem der Knoten gehört
        self.threshold_belive_p = threshold_belive_p        # Schwellenwert für positive Nachrichten
        self.neighbor = neighbor                            # Liste mit Relationship-Objekten


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
                conter_message) < self._threshold_belive(conter_message):
            pass
        return False


    ## Schwellenwert Glauben -> negative Nachrichten werden eher geglaubt werden
    def _threshold_belive(self, message):
        if message.get_mood():
            return self.threshold_belive_p
        if not message.get_mood():
            return self.threshold_belive_p/2



    ## Schwellwertüberschreitung Glauben
    def _threshold_ex_belive(self, message, time):
        return ((self.credibility(message, time) - self._threshold_belive) /
                (1 - self._threshold_belive))

    def nsi(self, message, time):
        pressure = 0

        for r in self.neighbor:
            nsi +=




    def isi(self, message):
