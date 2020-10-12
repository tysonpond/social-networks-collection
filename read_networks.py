import networkx as nx
import numpy as np
import re
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import json
import xml.etree.ElementTree as ET

NETWORKS_DIR = "NETWORKS/" # path to networks directory (change this if you move it)

def get_giant_component(G):
    # extract only the giant component
    cc = sorted(nx.connected_components(G), key=len, reverse=True)
    G.remove_nodes_from(set(G.nodes()) - set(cc[0]))
    return G


def read_adolescent():
    file = NETWORKS_DIR + "adolescent_health/out.moreno_health_health"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]   # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)
    
    G = nx.Graph()
    G.add_edges_from(elist)
    return G


def read_arxiv_CondMat():
    file = NETWORKS_DIR + "Arxiv_ca-CondMat/Newman-Cond_mat_95-99-binary.txt"
    elist = []
    with open(file, "r") as f:
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)

    return get_giant_component(G)


def read_arxiv_GrQc():
    file = NETWORKS_DIR + "Arxiv_ca-GrQc/CA-GrQc.txt"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(4)]  # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    
    return get_giant_component(G)


def read_ckm(network_num=3):
    assert network_num in [1,2,3], "network_num (int) must be 1, 2, or 3"
    file = NETWORKS_DIR + "CKM_physicians/ckm.txt"
    with open(file,"r") as f:
        skip = [next(f) for _ in range(9)]
        A123 = f.read().strip().split()
        N = 246
        A1 = A123[:N**2]
        A2 = A123[N**2:2*(N**2)]
        A3 = A123[2*(N**2):3*(N**2)]
        A1 = np.reshape(A1, (N,N)).astype(int)
        A2 = np.reshape(A2, (N,N)).astype(int)
        A3 = np.reshape(A3, (N,N)).astype(int)
        if network_num == 1:
            G = nx.from_numpy_matrix(A1)
        elif network_num == 2:
            G = nx.from_numpy_matrix(A2)
        else: #network_num == 3
            G = nx.from_numpy_matrix(A3)

    return get_giant_component(G)

    
def read_dolphins():
    file = NETWORKS_DIR + "dolphins/out.dolphins"
    elist = []
    with open(file, "r") as f:
        next(f, "")   # skip a line
        for line in f:
            e = set(int(x) for x in line.rstrip().split("\t"))
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    return G


def read_email():
    # Spain email network
    file = NETWORKS_DIR + "email_network/email.txt"
    elist = []
    with open(file, "r") as f:
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    return G


def read_enron():
    """ 10588 nodes
        65901 edges (directed) and   54527 (undirected)
        We use the undirected graph.
    """
    
    file = NETWORKS_DIR + "enron/enron-edgelist.txt"

    G = nx.read_edgelist(file, delimiter=" ", create_using=nx.Graph(),
                         data=False, encoding='utf-8')
    G = nx.convert_node_labels_to_integers(G, first_label=0)
    
    return get_giant_component(G)


def read_Eu_Core():
    file = NETWORKS_DIR + "email-Eu-core/email-Eu-core.txt"
    G = nx.read_edgelist(file,nodetype=int)

    return get_giant_component(G)


def read_Freemans(network_num=1):
    assert network_num in [1,2], "network_num (int) must be 1 or 2"
    file = NETWORKS_DIR + "Freemans_EIES/Freemans_EIES-time%i_n48.txt" % network_num
    elist = []
    with open(file, "r") as f:
        for line in f:
            e = set(int(x) for x in line.rstrip().split(" ")[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    return G


def read_golden():
    file = NETWORKS_DIR + "GoldenAge/HollywoodGoldenAge_matrix_s0.txt"
    A=np.loadtxt(file)
    G = nx.from_numpy_matrix(A)
    G.remove_edges_from(nx.selfloop_edges(G))
    return G


def read_hypertext():
    """ This network is a DYNAMIC network (edges are timestamped).
        We are treating it as static (a link is present if a
        link existed at any time).
    """
    file = NETWORKS_DIR + "sociopatterns-hypertext/out.sociopatterns-hypertext"
    elist = []
    with open(file,"r") as f:
        skip = [next(f) for _ in range(2)]
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    return G


def read_kapf():
    file = NETWORKS_DIR + "kapfdata/kapfts1.dat"
    adjmat = np.loadtxt(file)
    G = nx.from_numpy_matrix(adjmat)
    return G


def read_lesmis():
    # The downloaded file is not in proper GML format for Networkx
    # Run this once to reformat.
##    file = "../lesmis/lesmis.gml"
##    with open(file, "r") as f:
##        new_file_string = f.read().replace("\s+\[", "[")
##
##    with open("../lesmis/lesmis_reformatted.gml","w") as f:
##        f.write(new_file_string)

    file = NETWORKS_DIR + "lesmis/lesmis_reformatted.gml"
    G = nx.read_gml(file)
    G = nx.convert_node_labels_to_integers(G, first_label=0)
    return G


def read_Marvel():
    file = NETWORKS_DIR + "Marvel/Marvel.txt"
    elist = []
    with open(file,"r") as f:
        skip = [next(f) for _ in range(19430)]
        for line in f:
            linelist = line.rstrip().split()
            lineedges = [ (linelist[0], e2) for e2 in linelist[1:] ]
            elist.extend(lineedges)
    G = nx.Graph()
    G.add_edges_from(elist)
    G = nx.convert_node_labels_to_integers(G, first_label=0)

    return get_giant_component(G)


def read_movies():
    # Was unable to figure out how to use nx.read_pajek for this file,
    # ended up looking at the data and doing it manually. Edgelist starts
    # at line 107 and ends at line 298.
    file = NETWORKS_DIR + "movies/Movies.paj"
##    G = nx.read_pajek(file)
    elist = []
    with open(file,"r") as f:
        linecount = 1
        while linecount <= 298:
            line = f.readline()
            if linecount >= 107:
                line = re.sub(r'\s+', ' ', line).strip()
                e = set(int(x) for x in line.split(" ")[:2])
                elist.append(e)
                
            linecount += 1
            
    B = nx.Graph()
    B.add_edges_from(elist)
    B.add_node(78) # node 78 doesn't appear in any edges

    # Project onto composers. Two composers are linked if they worked with the
    # same producer.
    G = bipartite.projected_graph(B, list(range(63,103)))
    
    return get_giant_component(G)


def read_netscience():
    # The downloaded file is not in proper GML format for Networkx
    # Run this once to reformat.
##    file = NETWORKS_DIR + "netscience/netscience.gml"
##    with open(file, "r") as f:
##        new_file_string = f.read().replace("\s+\[", "[")
##
##    with open("../netscience/netscience_reformatted.gml","w") as f:
##        f.write(new_file_string)

    file = NETWORKS_DIR + "netscience/netscience_reformatted.gml"
    G = nx.read_gml(file)
    G = nx.convert_node_labels_to_integers(G, first_label=0)

    return get_giant_component(G)


def read_NFL():
    file = NETWORKS_DIR + "NFL2009_network/NFL2009_EdgeList.txt"
    elist = []
    with open(file, "r") as f:
        next(f, "")   # skip a line
        for line in f:
            e = set(int(x) for x in line.rstrip().split("\t")[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    
    return G


def read_org():
    file = NETWORKS_DIR + "organizational/Cross_Parker-Manufacturing_info.txt"
    elist = []
    with open(file, "r") as f:
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    return G


def read_pgp():
    file = NETWORKS_DIR + "pgp_trust/pgp_2004.net"
    elist = []
    with open(file,"r") as f:
        linecount = 1
        while linecount <= 35023:
            line = f.readline()
            if linecount >= 10684:
                e = tuple(int(x) for x in line.rstrip().split(" ")[:2])
                elist.append(e)
                
            linecount += 1
            
    G = nx.Graph()
    G.add_edges_from(elist)
    return G


def read_pgp2009():
    # # run this once to reformat raw data file. Make sure to gunzip the downloaded .gz file
    # file = NETWORKS_DIR + "pgp_trust2009/pgp-strong-2009.xml"
    # tree = ET.parse(file)  
    # root = tree.getroot()
    # prefix = "{http://graphml.graphdrawing.org/xmlns}"
    # graph = root.find(prefix + "graph")
    # edges = graph.findall(prefix + "edge")

    # sources, targets = [], []
    # for child in edges:
    #     edge = child.attrib # a dictionary with "source" and "target" as keys
    #                         # values can be n123 n44, indicating an edge 123-->44
    #     source = edge["source"].lstrip("n")
    #     target = edge["target"].lstrip("n")
    #     sources.append(source)
    #     targets.append(target)
    # # write a newly formatted file
    # new_file = NETWORKS_DIR + "pgp_trust2009/pgp-strong-2009.txt"
    # with open(new_file, "w") as f:
    #     for s,t in zip(sources, targets):
    #         f.write("{} {}\n".format(s,t))

    file = NETWORKS_DIR + "pgp_trust2009/pgp-strong-2009.txt"
    G = nx.read_edgelist(file, create_using=nx.Graph, nodetype=int)
    return G


### There is a better version of Sampson's monastery network. We will comment this one out.
##def read_Sampson_Pajek():
##    # Was unable to figure out how to use nx.read_pajek for this file,
##    # ended up looking at the data and doing it manually. Edgelist starts
##    # at line 107 and ends at line 298.
##    file = NETWORKS_DIR + "Sampson/Sampson.paj"
####    G = nx.read_pajek(file)
##    elist = []
##    with open(file,"r") as f:
##        linecount = 1
##        while linecount <= 350:
##            line = f.readline()
##            if linecount >= 29:
##                line = re.sub(r'\s+', ' ', line).strip()
##                relation = int(line.split(" ")[2]) # only keep positive links
##                e = set(int(x) for x in line.split(" ")[:2] if relation > -1)
##                
##                if len(e) == 2:
##                    elist.append(e)
##                
##            linecount += 1
##            
##    G = nx.Graph() 
##    G.add_edges_from(elist)
##    return G


def read_terrorist():
    file = NETWORKS_DIR + "terrorists/terrorist.pairs"
    G = nx.read_edgelist(file,nodetype=int)
    return G


def read_UC_Irvine():
    file = NETWORKS_DIR + "UC_Irvine2004/OClinks_w.txt"
    elist = []
    with open(file, "r") as f:
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)

    return get_giant_component(G)


def read_Arxiv_HepTh():
##    # The downloaded file is not in proper GML format for Networkx
##    # Run this once to reformat.
   # file = "Arxiv_ca-HepTh/hep-th.gml"
   # with open(file, "r") as f:
   #     new_file_string = f.read().replace("\s+\[", "[")

   # with open("Arxiv_ca-HepTh/hep-th_reformatted.gml","w") as f:
   #     f.write(new_file_string)

    file = NETWORKS_DIR + "Arxiv_ca-HepTh/hep-th_reformatted.gml"
    G = nx.read_gml(file)
    G = nx.convert_node_labels_to_integers(G, first_label=0)

    return get_giant_component(G)


def read_blogs():
    file = NETWORKS_DIR + "moreno_blogs/out.moreno_blogs_blogs"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    G.remove_edges_from(nx.selfloop_edges(G))
    
    return get_giant_component(G)


def read_club_membership():
    file = NETWORKS_DIR + "brunson_club-membership/out.brunson_club-membership_club-membership"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            line = line.rstrip().split()[:2]
            e = (int(line[0]),int(line[1])+25)
            elist.append(e)

    B = nx.Graph()
    B.add_edges_from(elist)

    # Project onto people. Two people are linked if they belong to the
    # same club/board.
    G = bipartite.projected_graph(B, list(range(1,26)))

##    # Project onto clubs.
##    G = bipartite.projected_graph(B, list(range(26,41)))
    
    return G


def read_facebook():
    file = NETWORKS_DIR + "ego-facebook/out.ego-facebook"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    
    return G


def read_gplus():
    file = NETWORKS_DIR + "ego-gplus/out.ego-gplus"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    
    return get_giant_component(G)


def read_highland():
    # signed network -- only take positive edges
    file = NETWORKS_DIR + "ucidata-gama/out.ucidata-gama"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            line = list(map(int,line.rstrip().split()))
            if line[2] == 1:
                e = (line[0],line[1])
                elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    
    return get_giant_component(G)


def read_highschool():
    file = NETWORKS_DIR + "moreno_highschool/out.moreno_highschool_highschool"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    
    return G


def read_jazz():
    file = NETWORKS_DIR + "arenas-jazz/out.arenas-jazz"
    elist = []
    with open(file, "r") as f:
        skip = next(f) # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    
    return G


def read_karate():
    file = NETWORKS_DIR + "ucidata-zachary/out.ucidata-zachary"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    
    return G


def read_prison():
    file = NETWORKS_DIR + "prison/prison.dat.txt"
    with open(file,"r") as f:
        skip = [next(f) for _ in range(4)]
        A = f.read().strip().split()
        N = 67
        A = np.reshape(A, (N,N)).astype(int)
        G = nx.from_numpy_matrix(A, create_using=nx.Graph())

    return G


def read_residence_oz():
    file = NETWORKS_DIR + "moreno_oz/out.moreno_oz_oz"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    
    return G


def read_Sampson():
    # signed network -- only take positive links
    file = NETWORKS_DIR + "moreno_sampson/out.moreno_sampson_sampson"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            line = list(map(int,line.rstrip().split()))
            if line[2] == 1:
                e = (line[0],line[1])
                elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    
    return G


def read_seventh():
    file = NETWORKS_DIR + "moreno_seventh/out.moreno_seventh_seventh"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    
    return G


def read_taro():
    file = NETWORKS_DIR + "moreno_taro/out.moreno_taro_taro"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    
    return G


def read_twitter():
    file = NETWORKS_DIR + "ego-twitter/out.ego-twitter"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    
    return get_giant_component(G)


def read_polbooks():
    # # run this once to reformat raw data file. Make sure to gunzip the downloaded .gz file
    # file = NETWORKS_DIR + "polbooks/polbooks.xml"
    # tree = ET.parse(file) #  
    # root = tree.getroot()
    # prefix = "{http://graphml.graphdrawing.org/xmlns}"
    # graph = root.find(prefix + "graph")
    # edges = graph.findall(prefix + "edge")

    # sources, targets = [], []
    # for child in edges:
    #     edge = child.attrib # a dictionary with "source" and "target" as keys
    #                         # values can be n123 n44, indicating an edge 123-->44
    #     source = edge["source"].lstrip("n")
    #     target = edge["target"].lstrip("n")
    #     sources.append(source)
    #     targets.append(target)
    # # write a newly formatted file
    # new_file = NETWORKS_DIR + "polbooks/polbooks.txt"
    # with open(new_file, "w") as f:
    #     for s,t in zip(sources, targets):
    #         f.write("{} {}\n".format(s,t))

    file = NETWORKS_DIR + "polbooks/polbooks.txt"
    G = nx.read_edgelist(file, create_using=nx.Graph, nodetype=int)
    return G


# dictionary that gives the corresponding read function
NETWORKS_DICT = {"Adolescent health": read_adolescent,
                "Arxiv CondMat": read_arxiv_CondMat,
                "Arxiv GrQc": read_arxiv_GrQc, 
                "CKM physicians": read_ckm,
                "Dolphins": read_dolphins,
                "Email Spain": read_email,
                "Email Enron": read_enron,
                "Email Eu Core": read_Eu_Core, 
                "Freeman's EIES": read_Freemans,
                "Golden Age": read_golden,
                "Hypertext": read_hypertext, 
                "Kapferer tailor": read_kapf,
                "Les Miserables": read_lesmis,
                "Marvel": read_Marvel, 
                "Hollywood music": read_movies,
                "Network science": read_netscience, 
                "NFL": read_NFL, 
                "Intra-organizational": read_org, 
                "Web of Trust": read_pgp,
                "Web of Trust (2009)": read_pgp2009, 
##                "Sampson's monastery": read_Sampson_Pajek, 
                "Terrorist": read_terrorist,
                "UC Irvine": read_UC_Irvine, 
                "Arxiv HepTh": read_Arxiv_HepTh, 
                "Blogs": read_blogs,
                "Club membership": read_club_membership,
                "Facebook": read_facebook,
                "Gplus": read_gplus,
                "Highland tribes": read_highland,
                "Highschool": read_highschool,
                "Prison": read_prison,
                "Jazz musicians": read_jazz,
                "Karate club": read_karate,
                "Residence hall": read_residence_oz,
                "Sampson's monastery": read_Sampson,
                "Seventh grade": read_seventh,
                "Taro exchange": read_taro,
                "Twitter": read_twitter,
                "Political books": read_polbooks}


# a list of small networks to test network algorithms on
SMALL_NETWORKS = ["CKM physicians", "Dolphins", "Freeman's EIES",
              "Golden Age", "Kapferer tailor", "Les Miserables",
              "Hollywood music", "Sampson's monastery", "Terrorist"]

def get_network_info(name):
    with open("network_descriptions.JSON", "r") as f:
        info = json.load(f)

    return info[name]

def read_any(name, print_info=False):        
    assert name in NETWORKS_DICT, "Name must be one of the following networks:\n" + "\n".join(sorted(NETWORKS_DICT.keys()))
    
    # print network info (description, citation, etc.) listed in network_descriptions.json
    if print_info == True:
        info = get_network_info(name) # get network info

        # format info and display
        print(name)
        lk = max([len(key) for key in info]) # longest key (most characters) for formatting purposes
        for key in info:
            print(" "*2, key.ljust(lk), "|", info[key])            

    return NETWORKS_DICT[name]()


if __name__ == "__main__":
    # visualize and print info for a small network
    G = read_any("Sampson's monastery", print_info=True)
    nx.draw(G)
    plt.show()