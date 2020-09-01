from read_networks import read_any, SMALL_NETWORKS
import community
from modularity import get_modularity
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import colorsys
import numpy as np

if __name__ == "__main__":
  # A plot of transitivity vs modularity
  x = []
  y = []
  for network in SMALL_NETWORKS:
     G = read_any(network)
     partition = community.best_partition(G)
     Q = get_modularity(G,partition)
     x.append(nx.transitivity(G))
     y.append(Q)
     print(network, Q)
  plt.plot(x,y,'o')
  plt.xlabel("Transitivity")
  plt.ylabel("Modularity")
  plt.show()
  # -------------------------------

  # Modularity maximization to identify & visualize top communities
  G = read_any("Network science")
  pos = nx.spring_layout(G, k=2/np.sqrt(nx.number_of_nodes(G)), iterations=100)
  partition = community.best_partition(G)
  print("#nodes: %i" % nx.number_of_nodes(G), 
      "#edges: %i" % nx.number_of_edges(G),
      "modularity (Q): %0.4f" % get_modularity(G,partition))

  # extract top communities and color them
  N = 8
  HSV_tuples = [(x*1.0/N, 1, 1) for x in range(N)]
  RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
  counts = [x[0] for x in Counter(list(partition.values())).most_common(N)]
  cmap = list(RGB_tuples)
  cols = []
  for node in G.nodes():
      if partition[node] in counts:
          cols.append(cmap[counts.index(partition[node])])
      else:
          cols.append('white')

  nodes = nx.draw_networkx_nodes(G, pos=pos, node_size=25, node_color=cols)
  edges = nx.draw_networkx_edges(G, pos=pos, edge_width=0.005, edge_color="#DEB992")
  ax = plt.axes()
  x='#051622'
  ax.spines["bottom"].set_color(x)
  ax.spines["top"].set_color(x)
  ax.spines["left"].set_color(x)
  ax.spines["right"].set_color(x)
  ax.set_facecolor(x)
  plt.show()