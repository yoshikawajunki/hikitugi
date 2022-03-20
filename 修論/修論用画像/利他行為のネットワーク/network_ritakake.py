#利他賭けの方向
import matplotlib.pyplot as plt
import networkx as nx


nodes = ['A','B','C','D','E','F','G','H','I','J']
#ノードの大きさは利他行為された回数
scores = [0.157480315,0.3149606299,0.9448818898,2.598425197,0.6299212598,2.755905512,0.3149606299,1.338582677,0.6299212598,0.3149606299]
colors = ["#ccddff"] * len(nodes)
styles = ["filled"] * len(nodes)

pos = {
'A': (40, 90),
'B': (60, 90),
'C': (10, 60),
'D': (30, 50),
'E': (10, 30),
'F': (75, 70),
'G': (90, 50),
'H': (80, 40),
'I': (50, 10),
'J': (70, 10)
}
# 各ノードに対応する情報を保存するため辞書として保存
new_nodes = { n : { "score" : scores[i], "pos" : pos[n], "color" : colors[i], "style" : styles[i] , "size" : scores[i] * 22  } for i, n in enumerate(nodes) }


edges = [
('A', 'C'),('A', 'D'),('A', 'E'),('A', 'G'),('A', 'J'),
('B', 'C'),('B', 'F'),('B', 'H'),
('C', 'A'),('C', 'B'),('C', 'D'),('C', 'E'),('C', 'F'),('C', 'G'),
('D', 'C'),('D', 'E'),('D', 'F'),('D', 'G'),('D', 'H'),('D', 'I'),
('E', 'D'),('E', 'F'),('E', 'H'),('E', 'I'),
('F', 'B'),('F', 'D'),('F', 'E'),('F', 'H'),('F', 'I'),
('G', 'D'),('G', 'F'),('G', 'H'),
('H', 'A'),('H', 'C'),('H', 'D'),('H', 'E'),('H', 'F'),('H', 'I'),
('I', 'D'),('I', 'E'),('I', 'F'),('I', 'H'),('I', 'J'),
('J', 'B'),('J', 'C'),('J', 'D'),('J', 'F'),('J', 'G'),('J', 'H'),
]
width = [5,3,2,1,2,1,6,5,1,2,5,1,3,1,1,2,5,1,1,3,3,6,2,2,1,6,1,3,1,4,5,3,1,2,3,1,4,2,8,1,1,1,1,1,3,1,4,1,2,1]
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
    nd.attr['width'] = new_nodes[n]["score"] 
    nd.attr['fillcolor'] = new_nodes[n]["color"]
    nd.attr['style'] = new_nodes[n]["style"]
    nd.attr['fontsize'] = new_nodes[n]["size"]
    nd.attr['pos'] = "{},{}!".format(new_nodes[n]["pos"][0] / 10, new_nodes[n]["pos"][1] / 10)


agraph.draw("network_ritakake.png", prog="neato", format="png")