import network_participant


class Bot(network_participant.Network_Participant):

    def __init__(self, np_id, threshold_believe_p, threshold_believe_n, turbulence_factor, indifference, isi_parameter, fi_parameter,
                 purchase_init_prob, purchase_prob_min, purchase_prob_max, purchase_expo_param_positive,
                 purchase_expo_param_negative, neighbors=None, send_box=None):

        super().__init__(np_id=np_id,
                         threshold_believe_p=threshold_believe_p,
                         threshold_believe_n=threshold_believe_n,
                         turbulence_factor=turbulence_factor,
                         indifference=indifference,
                         isi_parameter=isi_parameter,
                         fi_parameter=fi_parameter,
                         purchase_init_prob=purchase_init_prob,
                         purchase_prob_min=purchase_prob_min,
                         purchase_prob_max=purchase_prob_max,
                         purchase_expo_param_positive=purchase_expo_param_positive,
                         purchase_expo_param_negative=purchase_expo_param_negative,
                         neighbors=neighbors,
                         send_box=send_box)

    def _credibility(self, message, time):
        if message:
            if message.mood:
                return 1
        return 0

    def _forwarding_decision(self, message, counter_message, time, target):
        if message.mood:
            self.m_forwarding = True
            # self.n_m_forwarding += 1
            # self.prob_forwarding = self.n_m_forwarding / self.n_message
            return True
        return False

    def _purchase_int(self, message, counter_message, time):
        return 0

    def _purchase_decision(self, message, counter_message, time):
        return False
