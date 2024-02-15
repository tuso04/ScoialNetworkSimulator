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

    def __init__(self, simulation_runs, run_steps, network_params):
        self.simulation_runs = simulation_runs
        self.run_steps = run_steps
        self.network_params = network_params

        self.simulation_data = pd.DataFrame(columns=[
            "run",
            "prob_spreading",
            "avg_credibility",
            "prob_believe",
            "prob_forward",
            "prob_purchase",
            "avg_purchase"])

    def compute_simulation(self):
        for run in range(self.simulation_runs):
            new_run = self.compute_run(run)
            new_run.insert(0, "run", [run])
            self.simulation_data = pd.concat([self.simulation_data, new_run], ignore_index=True)
        self.simulation_data.to_csv(f"Simulation.csv")

    def compute_run(self, i):
        net_graph = network_generator.generate_new_network(shape=self.network_params["shape"],
                                                           n_nodes=self.network_params["n_nodes"],
                                                           init_edges=self.network_params["init_edges"],
                                                           split_prob=self.network_params["split_prob"])

        net = network.Network(net_graph,
                              n_influencer=self.network_params["n_influencer"],
                              n_bots=self.network_params["n_bots"],
                              message_start_time=self.network_params["message_start_time"],
                              counter_message_start_time=self.network_params["counter_message_start_time"],
                              turbulence_factor=self.network_params["turbulence_factor"])

        net.create_objects_from_graph()

        for time in range(self.run_steps):
            net.simulate_network(int(time))

        print(f"++++++++++++++++++++++++++++++++Ergebnisse{i}++++++++++++++++++++++++")
        print(net.simulation_data.tail(1))
        net.simulation_data.to_csv(f"Netzwerkübersicht{i}.csv")

        return net.simulation_data.tail(1)
