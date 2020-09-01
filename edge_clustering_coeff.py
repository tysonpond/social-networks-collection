import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from read_networks import read_any, SMALL_NETWORKS

def edge_clustering_coeff(G,u,v,return_info=False):
    u_nbrs = set(nx.neighbors(G,u))
    v_nbrs = set(nx.neighbors(G,v))
    uv_nbrs = u_nbrs & v_nbrs
    triangles = len(uv_nbrs)

    deg_u = len(u_nbrs)
    deg_v = len(v_nbrs)
    
    if min(deg_u-1,deg_v-1) == 0: # undefined?
        ECC = 0
    else:
        ECC = triangles/min(deg_u-1,deg_v-1)
    
    if return_info:
        return triangles, deg_u, deg_v, ECC
    else:
        return ECC

def get_all_ECCs(G):
    ECCs = []
    for i,e in enumerate(G.edges()):
        ECCs.append(edge_clustering_coeff(G,e[0],e[1]))
    return ECCs

if __name__ == "__main__":
    # ECC example from paper
    G = nx.Graph()
    G.add_edges_from([(1,2),(1,4),(1,5),(1,6),(2,3),(3,4),(3,5),(3,6),
                      (4,5),(4,6),(5,6)])
    print(edge_clustering_coeff(G,1,4))
    pos = nx.spring_layout(G)
    labels=nx.draw_networkx_labels(G,pos)
    nx.draw(G,pos)
    plt.show()

    # Test on real networks
    avg_ECC = []
    for name in SMALL_NETWORKS:
        G = read_any(name)
        ECCs = get_all_ECCs(G)
        avg_ECC.append(np.mean(ECCs))
    
    print("\n".join(["%s\t\t%0.3f" % (name,ECC) for name,ECC in zip(SMALL_NETWORKS,avg_ECC)]))
    
    # ECC distribution for a single network
    G = read_any("Network science")
    ECCs = get_all_ECCs(G)
    print("average clustering (node):", nx.average_clustering(G))
    print("average clustering (edge):", np.mean(ECCs))
    plt.hist(ECCs, bins="auto")
    plt.show()