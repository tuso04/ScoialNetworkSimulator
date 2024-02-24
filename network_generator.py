import random

import networkx as nx


def generate_new_network(shape, participant_params, n_nodes=1000, init_edges=6, split_prob=0.1, ):
    print("Beginne Generierung")

    if shape == "SFN":  # Scale-Free Network
        network_graph = nx.barabasi_albert_graph(n=n_nodes, m=init_edges)
    elif shape == "SWN":  # Small-World Network
        network_graph = nx.watts_strogatz_graph(n=n_nodes, k=init_edges, p=split_prob)
    else:
        network_graph = nx.gnm_random_graph(n=n_nodes, m=n_nodes * init_edges)

    turbulence_factor = 0.7

    nodes = network_graph.nodes()

    for i in range(len(nodes)):
        threshold_believe_p = random.normalvariate(participant_params["threshold_belive"], 1)
        indifference = random.normalvariate(participant_params["indifference"], 1)
        isi_parameter = random.normalvariate(participant_params["isi_parameter"], 1)
        fi_parameter = random.normalvariate(participant_params["fi_parameter"], 1)
        purchase_prob = random.normalvariate(participant_params["purchase_init_prob"], 1)
        purchase_prob_max = participant_params["purchase_prob_max"]
        purchase_prob_min = participant_params["purchase_prob_min"]
        purchase_expo_param_negative = participant_params["purchase_expo_param_positive"]
        purchase_expo_param_positive = participant_params["purchase_expo_param_negative"]

        nodes[i]["np_id"] = i
        nodes[i]["threshold_belive_p"] = threshold_believe_p
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
        nodes[i]["get_conter_message"] = 0
        nodes[i]["believe"] = False
        nodes[i]["forwarding"] = False
        nodes[i]["purchase"] = False

        """
        nodes[i]["object"] = network_participant.Network_Participant(np_id=i,
                                                                     network=net,
                                                                     threshold_believe_p=threshold_believe_p,
                                                                     indifference=indifference,
                                                                     isi_parameter=isi_parameter,
                                                                     fi_parameter=fi_parameter,
                                                                     purchase_prob=purchase_prob,
                                                                     neighbors=list(network_graph.neighbors(i))
                                                                     )
        """

    # Hinzufügen des Beziehungs-Attributs zu den Beziehungen
    bind = (0, 0)
    nx.set_edge_attributes(network_graph, bind, "bond")

    for e in network_graph.edges:
        network_graph.edges[e[0], e[1]]["bond"] = random.randint(0, 100) / 100, random.randint(0, 100) / 100

    # Umwandlung in JSON-Format
    json_data = nx.adjacency_data(network_graph)

    print("Netzwerk generiert!")

    return json_data


"""
net = network.Network(0.7)

n_json = generate_new_network(net, "SFN")

n = nx.adjacency_graph(n_json)

for i in range(len(n.nodes())):
    print(n.nodes()[i])
    print(n.nodes()[i]["object"].neighbors)

# degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
# dmax = max(degree_sequence)

fig = plt.figure("Random graph", figsize=(8, 8))
pos = nx.kamada_kawai_layout(n)

nx.draw_networkx_nodes(n, pos, node_size=20)
nx.draw_networkx_edges(n, pos, alpha=0.4)


fig.tight_layout()
plt.show()

"""

"""
ax0.set_title("Scale-Free Network G")
ax0.set_axis_off()
ax1 = fig.add_subplot(axgrid[3:, :2])
ax1.plot(degree_sequence, "b-", marker="o")
ax1.set_title("Degree Distribution Plot (2000 nodes)")
ax1.set_ylabel("Degree")
ax1.set_xlabel("Node Count")
ax2 = fig.add_subplot(axgrid[3:, 2:])
ax2.bar(*np.unique(degree_sequence, return_counts=True))
ax2.set_title("Degree histogram")
ax2.set_xlabel("Degree")
ax2.set_ylabel("Node Count")

"""
