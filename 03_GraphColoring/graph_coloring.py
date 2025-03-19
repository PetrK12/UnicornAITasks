import random

class GraphColoring:
    """Handles graph coloring operations."""
    
    def __init__(self, G, k, steps):
        self.G = G
        self.k = k
        self.steps = steps
        self.col = {node: random.randint(0, k-1) for node in G.nodes()}
        self.tabu_list = set()
        self.stagnation_count = 0
        self.max_stagnation = 500
    
    def is_valid_coloring(self):
        """Checks if the current coloring is valid."""
        for u, v in self.G.edges():
            if self.col[u] == self.col[v]:
                return False
        return True

    def find_conflicts(self):
        """Finds conflicting edges in the current coloring."""
        return [(u, v) for u, v in self.G.edges() if self.col[u] == self.col[v]]

    def resolve_conflicts(self, conflicts, step):
        u, v = random.choice(conflicts)
        node = random.choice([u, v])

        # Avoid tabu list cycles
        if all(n in self.tabu_list for edge in conflicts for n in edge):
            self.tabu_list.clear()
        if node in self.tabu_list:
            return

        # Select the least conflicting color
        color_counts = {c: 0 for c in range(self.k)}
        for neighbor in self.G.neighbors(node):
            if self.col[neighbor] in color_counts:
                color_counts[self.col[neighbor]] += 1

        min_conflict = min(color_counts.values())
        best_colors = [c for c in color_counts if color_counts[c] == min_conflict]
        new_color = random.choice(best_colors)

        if self.col[node] == new_color:
            self.stagnation_count += 1
        else:
            self.stagnation_count = 0  # Reset stagnation counter
        
        self.col[node] = new_color
        self.tabu_list.add(node)
        
        # Limit the tabu list size
        if len(self.tabu_list) > 10:
            self.tabu_list.pop()

        # Reset tabu list if stagnation occurs
        if self.stagnation_count >= self.max_stagnation:
            self.tabu_list.clear()
            self.stagnation_count = 0

        # Introduce mutation to escape local optima
        mutation_rate = 0.1 if step < self.steps // 2 else 0.3
        if random.random() < mutation_rate:
            rand_node = random.choice(list(self.G.nodes()))
            self.col[rand_node] = random.randint(0, self.k-1)

    def color_graph(self):
        """Runs local search to find a valid coloring."""
        for step in range(self.steps):
            conflicts = self.find_conflicts()
            if not conflicts:
                return self.col, True, step  # Found a valid coloring
            self.resolve_conflicts(conflicts, step)
        return self.col, False, -1  # Failed to find valid coloring