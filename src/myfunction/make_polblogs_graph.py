import networkx as nx
import csv
from collections import defaultdict

edge_path = "data/polblogs/edges.csv"
nodes_path = "data/polblogs/nodes.csv"

def make_polblogs_graph(edge_path: str = edge_path, node_path: str = nodes_path) -> nx.Graph():
    with open(node_path) as f:
        reader = csv.reader(f)
        l = [row for row in reader]

    nodes_header = l[0]
    # ヘッダー以外をスライス
    l = l[1:]
    print("header information")
    print(l[0])

    # networkxでネットワーク構成してからな方が良さそう
    # 理由は，今回使う隣接行列が自己ループは二倍にするという制約がありこれは一般性のある制約じゃない気がするから
    ture_community = []
    N = len(l)

    print(f"ノード数:{N}")

    for i in range(N):
        ture_community.append(int(l[i][3]))

    print(f"ture_communityの配列のサイズ:{len(ture_community)}")

    G = nx.Graph()
    G.add_nodes_from([i for i in range(N)])

    with open(edge_path) as f:
        reader = csv.reader(f)
        e = [row for row in reader]

    header_e = e[0]
    e = e[1:]

    edges = [[int(v) for v in row] for row in e]
    # len(edges)

    edge_wight = defaultdict(int)

    for edge in edges:
        if edge[0] > edge[1]:
            key = (edge[1], edge[0])
        else:
            key = (edge[0], edge[1])
        edge_wight[key] += 1

    d = defaultdict(int)

    for key, value in edge_wight.items():
        d[value] += 1

    print(d)

    for key, value in edge_wight.items():
        source, target = key
        G.add_edge(source, target, weight = value)
    
    return G,ture_community
