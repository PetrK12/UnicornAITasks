import networkx as nx # type: ignore
import json
import os
import numpy as np # type: ignore

class GraphIO:
    """Handles reading and writing graph-related data."""
    
    @staticmethod
    def read_dimacs(filename):
        """Reads a graph from a DIMACS file format."""
        G = nx.Graph()
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith("e"):
                    vs = [int(s) for s in line.split() if s.isdigit()]
                    G.add_edge(vs[0]-1, vs[1]-1)
        return G
    
    @staticmethod
    def save_results(filename, graph_name, result):
        """Appends graph coloring results to a JSON file."""
        data = {
            "Graph": graph_name,
            "Success": result[1],
            "Colors": result[0],
            "Steps": result[2],
            "NumberOfColors": len(set(result[0].values())) 
        }

        # Load existing data if the file exists
        if os.path.exists(filename):
            with open(filename, "r") as file:
                existing_data = json.load(file)
        else:
            existing_data = []
        
        existing_data.append(data)
        
        with open(filename, "w") as file:
            json.dump(existing_data, file, indent=4)