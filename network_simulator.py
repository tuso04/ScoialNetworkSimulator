import pandas as pd

import network
import network_generator

"""network_parameters = {
    "shape": "SWN",
    "n_nodes": 10,
    "init_edges": 4,
    "split_prob": 0.1,
    "turbulence_factor": 0.7,
    "n_bots": 2,
    "n_influencer": 4
}"""


class Network_Simulation:

    def __init__(self, sim_params, network_params, participant_params, message_params, counter_message_params):

        # Simulationsparameters
        self.simulation_runs = sim_params["runs"]
        self.run_steps = sim_params["run_steps"]
        self.get_run_csv = sim_params["run_csv"]

        self.network_params = network_params
        self.participant_params = participant_params
        self.message_params = message_params
        self.counter_message_params = counter_message_params

        self.simulation_data = pd.DataFrame(columns=[
            "run",
            "prob_spreading",
            "prob_counter_spreading",
            "avg_credibility",
            "avg_counter_credibility",
            "prob_believe",
            "prob_counter_believe",
            "prob_forward",
            "prob_counter_forward",
            "prob_purchase",
            "avg_purchase"])

    def compute_simulation(self):
        for run in range(self.simulation_runs):
            new_run = self._compute_run(run)
            new_run.insert(0, "run", [run])
            self.simulation_data = pd.concat([self.simulation_data, new_run], ignore_index=True)
            self.simulation_data.rename(columns={"run": "Durchlauf",
                                                 "prob_spreading": "Verbreitung der Nachricht",
                                                 "prob_counter_spreading": "Verbreitung Gegennachricht",
                                                 "avg_credibility": "Durchschnittliche Glaubwürdigkeit (Nachricht)",
                                                 "avg_counter_credibility": "Durchschnittliche Glaubwürdigkeit (Gegennachricht)",
                                                 "prob_believe": "Anteil Teilnehmer die Nachricht glauben",
                                                 "prob_counter_believe": "Anteil Teilnehmer die Gegennachricht glauben",
                                                 "prob_forward": "Anteil Weiterleitung (Nachricht)",
                                                 "prob_counter_forward": "Anteil Weiterleitung (Gegennachricht)",
                                                 "prob_purchase": "Anteil Teilnehmer die Produkt kaufen wollen",
                                                 "avg_purchase": "Durchschnittliche Kaufwahrscheinlichkeit"})
            self.simulation_data.to_csv(f"Simulation.csv")
        return self.simulation_data

    def _compute_run(self, i):
        net_graph = network_generator.generate_new_network(shape=self.network_params["shape"],
                                                           participant_params=self.participant_params,
                                                           n_nodes=self.network_params["n_nodes"],
                                                           init_edges=self.network_params["init_edges"],
                                                           split_prob=self.network_params["split_prob"])

        net = network.Network(net_graph,
                              n_influencer=self.network_params["n_influencer"],
                              n_bots=self.network_params["n_bots"],
                              message_params=self.message_params,
                              counter_message_params=self.counter_message_params,
                              turbulence_factor=self.network_params["turbulence_factor"])

        net.create_objects_from_graph()

        for time in range(self.run_steps):
            net.simulate_network(int(time))

        print(f"++++++++++++++++++++++++++++++++Ergebnisse{i}++++++++++++++++++++++++")
        print(net.simulation_data.tail(1))

        if self.get_run_csv:
            net.simulation_data.to_csv(f"Netzwerkübersicht{i}.csv")

        return net.simulation_data.tail(1)
