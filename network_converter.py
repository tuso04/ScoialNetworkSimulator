import json
import networkx as nx

import network


def network_form_json(json_file):
    # Wandle JSON-Daten in networkx-Graph um
    network_graph = nx.adjacency_graph(json_file)

    # Erstelle Netzwerk-Objekt
    current_network = network.Network(network_graph, turbulence_factor=0.7)  # Umgang mit Turbulenz-Factor klären
    return current_network

