import networkx as nx
import numpy as np

class GraphPlotter:
    """Handles graph plotting operations."""
    
    @staticmethod
    def plot(G, cols):
        """Plots a colored graph."""
        rng = np.random.default_rng(12345)
        k = max(cols)
        symbols = '0123456789ABCDEF'
        colmap = ["#" + ''.join(rng.choice(list(symbols), 6)) for _ in range(k+1)]
        colors = [colmap[c] for c in cols]
        nx.draw(G, node_color=colors, with_labels=True)
