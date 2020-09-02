from read_networks import read_any, NETWORKS_DICT, SMALL_NETWORKS
import numpy as np
import pandas as pd
import networkx as nx
import community
from modularity import get_modularity

def display_basic_network_stats(network_list):
    print("Network".ljust(22), "N".ljust(5), "E".ljust(5), "dens".ljust(7), "C".ljust(7), "r".ljust(7), "cc")

    for name in network_list:
        G = read_any(name)
        G.remove_edges_from(nx.selfloop_edges(G))
        cc = sorted(nx.connected_components(G), key=len, reverse=True)
        print(name.ljust(22),
              str(nx.number_of_nodes(G)).ljust(5),
              str(nx.number_of_edges(G)).ljust(5),
              ("%0.4f" % nx.density(G)).ljust(7),
              ("%0.4f" % nx.transitivity(G)).ljust(7),
              ("%0.4f" % nx.degree_assortativity_coefficient(G)).ljust(7),
              len(cc))

STATS_DICT = {"num_nodes": nx.number_of_nodes,
			  "num_edges": nx.number_of_edges,
			  "density": nx.density,
			  "transitivity": nx.transitivity,
			  "avg_clustering": nx.average_clustering,
			  "avg_k": lambda G: 2*nx.number_of_edges(G)/nx.number_of_nodes(G),
			  "min_k": lambda G: min([deg for node,deg in G.degree()]),
			  "max_k": lambda G: max([deg for node,deg in G.degree()]),
			  "ASPL": nx.average_shortest_path_length,
			  "diameter": nx.diameter,
			  "assortativity": nx.degree_assortativity_coefficient,
			  "modularity": lambda G: get_modularity(G,community.best_partition(G))
}

def fill_nan(nrows,ncols):
    a = np.empty((nrows,ncols))
    a.fill(np.nan)
    return a
 
def save_network_stats_table(network_list, stats_list, outfile, round_to=3, sort_by="density", print_latex=True):

	assert len(set(stats_list) - set(STATS_DICT.keys())) == 0, print("stats list can only contain these functions:\n%s" % "\n".join(STATS_DICT.keys()))
	nrows = len(network_list)
	ncols = len(stats_list)
	data = fill_nan(nrows, ncols)
	
	for i,name in enumerate(network_list):
		print("Computing stats for: ", name)
		G = read_any(name, print_info=False)

		for j,stat in enumerate(stats_list):
			stat_val = STATS_DICT[stat](G)
			data[i,j] = round(stat_val, round_to)

	df = pd.DataFrame(data, columns= stats_list, index=network_list)
	df.index.name = "Network" 
	df = df.sort_values(sort_by)

	with open(outfile, "w", newline = "\n") as f:
		f.write(df.to_csv())

	# print LaTeX table
	if print_latex == True:
		print("\n")
		with open(outfile,"r") as f:
			dfstring = f.read()
			dfstring = dfstring.replace(",", " & ")
			dfstring = dfstring.replace("\n", r"\\" + "\n")
		
		dfstring = dfstring.strip().lstrip("& ").rstrip(r"\\") + "\n"
		head = "\\begin{tabular}{" + "l|" + "l"*ncols + "}\n"
		end = "\\end{tabular}"
		print(head + dfstring + end)

if __name__ == "__main__":
	# print basic stats for all networks
    display_basic_network_stats(sorted(NETWORKS_DICT.keys()))

	# save full stats for smaller networks & print LaTeX table
    save_network_stats_table(SMALL_NETWORKS, STATS_DICT.keys(), "small_networks_stats.csv",
		round_to=3, sort_by="density", print_latex=True)