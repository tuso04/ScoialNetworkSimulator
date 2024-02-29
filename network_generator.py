import random

import networkx as nx


def generate_new_network(shape, participant_params, n_nodes, init_edges, split_prob):
    if shape == "SFN":  # Scale-Free Network
        network_graph = nx.barabasi_albert_graph(n=n_nodes, m=init_edges)
    elif shape == "SWN":  # Small-World Network
        network_graph = nx.watts_strogatz_graph(n=n_nodes, k=init_edges, p=split_prob)
        print(nx.average_shortest_path_length(network_graph))
        print(nx.average_clustering(network_graph))
    else:
        network_graph = nx.gnm_random_graph(n=n_nodes, m=n_nodes * init_edges)

    # Liste mit Knoten des Netzwerks
    nodes = network_graph.nodes()

    for i in range(len(nodes)):

        # Zufällige Erzeugung der Teilnehmerparameter mit Normalverteilung
        threshold_believe_p = random.normalvariate(participant_params["threshold_believe"], 0.125)
        threshold_believe_n = random.normalvariate(participant_params["threshold_believe"]/2, 0.0625)
        turbulence_factor = random.normalvariate(participant_params["turbulence_factor"], 0.125)
        indifference = random.normalvariate(participant_params["indifference"], 1)
        isi_parameter = random.normalvariate(participant_params["isi_parameter"], 0.125)
        fi_parameter = random.normalvariate(participant_params["fi_parameter"], 1)
        purchase_prob = participant_params["purchase_init_prob"]  # random.normalvariate(participant_params["purchase_init_prob"], 1)
        purchase_prob_max = participant_params["purchase_prob_max"]
        purchase_prob_min = participant_params["purchase_prob_min"]
        purchase_expo_param_negative = participant_params["purchase_expo_param_positive"]
        purchase_expo_param_positive = participant_params["purchase_expo_param_negative"]

        nodes[i]["np_id"] = i
        nodes[i]["threshold_believe_p"] = threshold_believe_p
        nodes[i]["threshold_believe_n"] = threshold_believe_n
        nodes[i]["turbulence_factor"] = turbulence_factor
        nodes[i]["indifference"] = indifference
        nodes[i]["isi_parameter"] = isi_parameter
        nodes[i]["fi_parameter"] = fi_parameter
        nodes[i]["purchase_prob"] = purchase_prob
        nodes[i]["purchase_prob_max"] = purchase_prob_max
        nodes[i]["purchase_prob_min"] = purchase_prob_min
        nodes[i]["purchase_prob_negative"] = purchase_expo_param_negative
        nodes[i]["purchase_prob_positive"] = purchase_expo_param_positive
        nodes[i]["send_box"] = None
        nodes[i]["get_message"] = 0
        nodes[i]["get_counter_message"] = 0
        nodes[i]["believe"] = False
        nodes[i]["forwarding"] = False
        nodes[i]["purchase"] = False

    # Hinzufügen des Beziehungs-Attributs zu den Beziehungen
    bind = (0, 0)
    nx.set_edge_attributes(network_graph, bind, "bond")

    for e in network_graph.edges:
        network_graph.edges[e[0], e[1]]["bond"] = random.randint(0, 100) / 100, random.randint(0, 100) / 100

    # Umwandlung in JSON-Format
    json_data = nx.adjacency_data(network_graph)

    print("Netzwerk generiert!")

    return json_data
