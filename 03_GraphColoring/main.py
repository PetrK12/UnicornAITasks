from graph_io import GraphIO
from graph_coloring import GraphColoring
from graph_plotter import GraphPlotter

"""Main execution function for graph coloring."""
input_files = ['dsjc125.9.col.txt', 'dsjc125.1.col.txt']
colors_needed = [44, 5]
steps = [1_000_000, 400_000]
output_file = "results.json"

for i, filename in enumerate(input_files):
    G = GraphIO.read_dimacs(filename)
    graph_coloring = GraphColoring(G, colors_needed[i], steps[i])
    result = graph_coloring.color_graph()
        
    print(f"{filename} success:", result[1], "Steps:", result[2])
        
    #GraphPlotter.plot(G, list(result[0]))
    GraphIO.save_results(output_file, filename, result)
