import network
import network_generator
import network_simulator

"""for i in range(10):
    net_graph = network_generator.generate_new_network("SWN", 10, init_edges=4)

    net = network.Network(net_graph, turbulence_factor=0.7)

    net.create_objects_from_graph()

    for time in range(10):
        net.simulate_network(int(time))

    print(f"++++++++++++++++++++++++++++++++Ergebnisse{i}++++++++++++++++++++++++")
    print(net.simulation_data)
    net.simulation_data.to_csv(f"Netzwerküberischt{i}.csv")"""

network_parameters = {}
participant_parameters = {}
message_parameters = {}
counter_message_parameters = {}
simulation_parameters = {}

network_parameters["shape"] = 'SWN'
network_parameters["n_nodes"] = 1000
network_parameters["init_edges"] = 6
network_parameters["split_prob"] = 0.1
network_parameters["turbulence_factor"] = 0
network_parameters["n_bots"] = 0
network_parameters["n_influencer"] = 0

participant_parameters["threshold_believe"] = 0.5
participant_parameters["indifference"] = 0.1
participant_parameters["isi_parameter"] = 0.5
participant_parameters["fi_parameter"] = 0.5
participant_parameters["purchase_init_prob"] = 0.1
participant_parameters["purchase_prob_max"] = 0.125
participant_parameters["purchase_prob_min"] = 0.05
participant_parameters["purchase_expo_param_positive"] = 5
participant_parameters["purchase_expo_param_negative"] = 2.5

message_parameters["check"] = True
message_parameters["start_time"] = 0
message_parameters["life_time"] = 20
message_parameters["quality"] = 0.3
message_parameters["emotionality"] = 0.3

counter_message_parameters["check"] = True
counter_message_parameters["start_time"] = 0
counter_message_parameters["life_time"] = 20
counter_message_parameters["quality"] = 0.3
counter_message_parameters["emotionality"] = 0.3

simulation_parameters["runs"] = 20
simulation_parameters["run_steps"] = 150
simulation_parameters["run_csv"] = True

ns = network_simulator.Network_Simulation(simulation_parameters,
                                          network_parameters,
                                          participant_parameters,
                                          message_parameters,
                                          counter_message_parameters)

simulation_csv = ns.compute_simulation()
simulation_csv.to_csv("TestSimulation.csv")


print(simulation_csv)
