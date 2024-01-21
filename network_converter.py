import json
import networkx as nx

import network

def network_form_json(json_file):

    # Lese JSON Daten aus Datei
    with open(json_file, "r") as js_f:
        json_network_graph = json.load(js_f)

    # Wandle JSON-Daten in networkx-Graph um
    network_graph = nx.adjacency_graph(json_network_graph)

    # Erstelle Netzwerk-Objekt
    current_network = network.Network(network_graph, turbulence_factor=0.7) # Umgang mit Turbulenz-Factor klären
    return current_network


network_form_json("network.json")

