#利他賭けの方向
import matplotlib.pyplot as plt
import networkx as nx


nodes = ['B','A']
#ノードの大きさは利他行為された回数
scores = [1,1]
colors = ["#ccddff"] * len(nodes)
styles = ["filled"] * len(nodes)

pos = {
'A': (10, 30),
'B': (30, 30),

}


# 各ノードに対応する情報を保存するため辞書として保存
new_nodes = { n : { "score" : scores[i], "pos" : pos[n], "color" : colors[i], "style" : styles[i] } for i, n in enumerate(nodes) }


edges = [
('B', 'A')
]

width = [10]
# エッジもノードと同様辞書として保存
new_edges = { e : width[i] for i, e in enumerate(edges) }


G = nx.MultiDiGraph()
# 頂点の追加
for n, attr in new_nodes.items():
    G.add_node(n)

# 辺の追加 (頂点も必要に応じて追加されます)
G.add_edges_from(new_edges.keys())

agraph = nx.nx_agraph.to_agraph(G)
agraph.node_attr["shape"] = "circle"
for (i, j) in G.edges():
    edge = agraph.get_edge(i, j)
    edge.attr['penwidth'] = new_edges[(i, j)] / 2

for n in G.nodes():
    nd = agraph.get_node(n)
    nd.attr['fillcolor'] = new_nodes[n]["color"]
    nd.attr['style'] = new_nodes[n]["style"]
    nd.attr['pos'] = "{},{}!".format(new_nodes[n]["pos"][0] / 10, new_nodes[n]["pos"][1] / 10)


agraph.draw("network_test.png", prog="neato", format="png")
