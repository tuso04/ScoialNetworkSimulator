import random

import networkx as nx
import matplotlib.pyplot as plt

import network_participant
import network


def generate_new_network(shape, turbulence_factor, n_nodes=200, init_edges=2, split_prob=0.1):
    if shape == "SFN":  # Scale-Free Network
        network_graph = nx.barabasi_albert_graph(n=n_nodes, m=init_edges)
    elif shape == "SWN":  # Small-World Network
        network_graph = nx.watts_strogatz_graph(n=n_nodes, k=init_edges, p=split_prob)
    else:
        network_graph = nx.gnm_random_graph(n=n_nodes, m=n_nodes * init_edges)

    net = network.Network(graph=network_graph,
                          turbulence_factor=turbulence_factor)

    nodes = network_graph.nodes()

    for i in range(len(nodes)):
        threshold_belive_p = random.randint(1, 100) / 100,
        indifference = random.randint(1, 100) / 100,
        isi_parameter = random.randint(1, 100) / 100,
        fi_parameter = random.randint(1, 100) / 100,
        purchase_prob = random.randint(1, 100) / 100,

        nodes[i]["id"] = i
        nodes[i]["object"] = network_participant.Network_Participant(np_id=i,
                                                                     network=net,
                                                                     threshold_belive_p=threshold_belive_p,
                                                                     indifference=indifference,
                                                                     isi_parameter=isi_parameter,
                                                                     fi_parameter=fi_parameter,
                                                                     purchase_prob=purchase_prob,
                                                                     neighbors=list(network_graph.neighbors(i))
                                                                     )
        print(nodes[i])

    return network_graph


n = generate_new_network("SFN", turbulence_factor=0.7)

# degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
# dmax = max(degree_sequence)

fig = plt.figure("Random graph", figsize=(8, 8))
pos = nx.kamada_kawai_layout(n)

nx.draw_networkx_nodes(n, pos, node_size=20)
nx.draw_networkx_edges(n, pos, alpha=0.4)

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

fig.tight_layout()
plt.show()