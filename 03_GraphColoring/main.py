from graph_io import GraphIO # type: ignore
from graph_coloring import GraphColoring # type: ignore
from graph_plotter import GraphPlotter # type: ignore

"""Main execution function for graph coloring."""
input_files = ['dsjc125.9.col.txt', 'dsjc125.1.col.txt']
colors_needed = [44, 5]
steps = [1_000_000, 400_000]
output_file = "results.json"

for i, filename in enumerate(input_files):
    G = GraphIO.read_dimacs(filename)
    graph_coloring = GraphColoring(G, colors_needed[i], steps[i])
    result = graph_coloring.color_graph()
    
    print(f"{filename} succesfully found solution:", result[1], "Steps:", result[2])
    print(f"Solution valid: {graph_coloring.is_valid_coloring()}")    

    #GraphPlotter.plot(G, list(result[0]))
    GraphIO.save_results(output_file, filename, result)
