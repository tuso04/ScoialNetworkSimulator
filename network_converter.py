import json
import networkx as nx

import network


def network_form_json(json_file):
    # Wandle JSON-Daten in networkx-Graph um

    # Erstelle Netzwerk-Objekt
    current_network = network.Network(json_file, turbulence_factor=0.7)  # Umgang mit Turbulenz-Factor klären
    return current_network

