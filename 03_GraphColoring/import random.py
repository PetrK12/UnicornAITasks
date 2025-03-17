import random
import networkx as nx 

Gd = nx.Graph()

def readdimacs(filename):

    file = open(filename, 'r')
    lines = file.readlines()
    
    Gd = nx.Graph()

    for line in lines:
        if line[0] == "e":
            vs = [int(s) for s in line.split() if s.isdigit()]
            Gd.add_edge(vs[0]-1, vs[1]-1)
    return Gd

G1 = readdimacs('dsjc125.9.col.txt')  

def color(G, k, steps):
    """Použije lokální prohledávání k nalezení obarvení grafu G pomocí k barev."""
    # Inicializace náhodného obarvení
    col = {node: random.randint(0, k-1) for node in G.nodes()}
    tabu_list = set()
    stagnation_count = 0  # Počítadlo stagnace
    max_stagnation = 500  # Po kolika krocích se resetuje tabu list
    
    for step in range(steps):
        conflicts = [(u, v) for u, v in G.edges() if col[u] == col[v]]
        if not conflicts:
            return col, True  # Našli jsme validní obarvení
        
        # Pokud zbývá méně než 3 konfliktní hrany, ignorujeme tabu list
        if len(conflicts) < 3:
            tabu_list.clear()
        
        # Vybereme náhodný konfliktní vrchol
        u, v = random.choice(conflicts)
        node = random.choice([u, v])
        
        # Pokud všechny konfliktní vrcholy jsou v tabu listu, resetujeme tabu list
        if all(n in tabu_list for edge in conflicts for n in edge):
            tabu_list.clear()
        
        # Pokud je uzel v tabu listu, vybereme jiný
        if node in tabu_list:
            continue
        
        # Změníme jeho barvu na nejméně konfliktní
        color_counts = {c: 0 for c in range(k)}
        for neighbor in G.neighbors(node):
            if col[neighbor] in color_counts:
                color_counts[col[neighbor]] += 1
        
        # Vybereme barvu s nejnižším konfliktem (s váženým výběrem)
        min_conflict = min(color_counts.values())
        best_colors = [c for c in color_counts if color_counts[c] == min_conflict]
        new_color = random.choice(best_colors)
        
        # Pokud se barva nemění, zvyšujeme stagnaci
        if col[node] == new_color:
            stagnation_count += 1
        else:
            stagnation_count = 0  # Reset stagnace při změně
        
        col[node] = new_color
        
        # Přidáme vrchol do tabu listu, abychom zabránili cyklení
        tabu_list.add(node)
        if len(tabu_list) > 10:  # Omezíme velikost tabu listu
            tabu_list.pop()
        
        # Reset tabu listu při stagnaci
        if stagnation_count >= max_stagnation:
            tabu_list.clear()
            stagnation_count = 0
        
        # Dynamická mutace (zvyšujeme šanci při stagnaci)
        mutation_rate = 0.1 if step < steps // 2 else 0.3
        if random.random() < mutation_rate:
            rand_node = random.choice(list(G.nodes()))
            col[rand_node] = random.randint(0, k-1)
    
    return col, False  # Nepodařilo se najít validní obarvení

# Načtení grafů a testování
#G1 = nx.read_edgelist("dsjc125.9.col", nodetype=int)
#G2 = nx.read_edgelist("dsjc125.1.col", nodetype=int)

result1 = color(G1, 50, 1000000)
#result2 = color(G2, 5, 100000)

print("G1 success:", result1[1])
#print("G2 success:", result2[1])
