class Network_Participant:
    def __init__(self, network, threshold_belive_p):
        self._network = network
        self._threshold_belive_p = threshold_belive_p


    ## Glaubwürdigkeit (Cm/it)
    def credibility(self, message, time):
        credibility = (self._network.get_turbulence_factor*self.nsi(message, time)+
                           (1-self._network.get_turbulence_factor)*self.isi(message, time))
        return credibility

    ## Glauben
    def belive(self,message, conter_message, time):
        threshold_ex_message = self._threshold_ex_belive(message, time)
        threshold_ex_conter_message = self._threshold_ex_belive(conter_message, time)

        if threshold_ex_message > threshold_ex_conter_message:
            return message
        return None

    ## Entscheidung !!! Frage zur Entscheidung
    def decision(self, message, conter_message, time):
        decision = self.belive(message, conter_message, time)

        if decision == None:
            if self.credibility(message, time) >= self._threshold_belive(message) and self.credibility(conter_message) < self._threshold_belive(conter_message):
                return self.belive(message, conter_message, time)
            if self.credibility(message, time) >= self._threshold_belive(message) and self.credibility(conter_message) < self._threshold_belive(conter_message) and :


    ## Schwellenwert Glauben -> negative Nachrichten werden eher geglaubt werden
    def _threshold_belive(self, message):
        if message.get_mood():
            return self._threshold_belive_p
        if not message.get_mood():
            return self._threshold_belive_p/2



    ## Schwellwertüberschreitung Glauben  !!!Noch zu implementieren, dass !!!
    def _threshold_ex_belive(self, message, time):
        return ((self.credibility(message, time) - self._threshold_belive) /
                (1 - self._threshold_belive))

    def nsi(self, message):

    def isi(self, message):
