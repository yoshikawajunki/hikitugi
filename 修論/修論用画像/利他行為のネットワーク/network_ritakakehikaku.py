#賭けの方向を表している
#かけられた回数をされた回数を紫のノードの大きさで表し、利他行為した回数を赤丸で表している。
import matplotlib.pyplot as plt
import networkx as nx


nodes = ['A','C','D','E','F','G','H','I','J','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ',]
#ノードの大きさは利他行為された回数
scores = [0.7894736842,1.842105263,2.236842105,0.3947368421,2.236842105,0.7894736842,0.9210526316,0.3947368421,0.3947368421,0.157480315,0.3149606299,0.9448818898,2.598425197,0.6299212598,2.755905512,0.3149606299,1.338582677,0.6299212598,0.3149606299]
colors = ["#ff6347" , "#ff6347" ,  "#ff6347" ,  "#ff6347" ,  "#ff6347" ,  "#ff6347" ,  "#ff6347" ,  "#ff6347" ,  "#ff6347" ,"#661065" , "#661065" , "#661065" , "#661065" , "#661065" ,  "#661065" , "#661065" , "#661065" ,  "#661065" , "#661065"  ]
styles = ["filled"] * len(nodes)

pos = {
'A': (40, 90),
'C': (10, 70),
'D': (30, 50),
'E': (10, 30),
'F': (75, 70),
'G': (90, 50),
'H': (80, 40),
'I': (50, 10),
'J': (70, 10),
'AA': (40, 90),
'AB': (60, 90),
'AC': (10, 70),
'AD': (30, 50),
'AE': (10, 30),
'AF': (75, 70),
'AG': (90, 50),
'AH': (80, 40),
'AI': (50, 10),
'AJ': (70, 10)
}
# 各ノードに対応する情報を保存するため辞書として保存
new_nodes = { n : { "score" : scores[i], "pos" : pos[n], "color" : colors[i], "style" : styles[i] ,"size" : 0 } for i, n in enumerate(nodes) }


edges = [
('A', 'C'),('A', 'AD'),('A', 'AE'),('A', 'G'),('A', 'J'),
('AB', 'C'),('AB', 'AF'),('AB', 'AH'),
('C', 'A'),('C', 'AB'),('C', 'AD'),('C', 'AE'),('C', 'AF'),('C', 'G'),
('AD', 'C'),('AD', 'AE'),('AD', 'AF'),('AD', 'G'),('AD', 'AH'),('AD', 'AI'),
('AE', 'AD'),('AE', 'AF'),('AE', 'AH'),('AE', 'AI'),
('AF', 'AB'),('AF', 'AD'),('AF', 'AE'),('AF', 'AH'),('AF', 'AI'),
('G', 'AD'),('G', 'AF'),('G', 'AH'),
('AH', 'A'),('AH', 'C'),('AH', 'AD'),('AH', 'AE'),('AH', 'AF'),('AH', 'AI'),
('AI', 'AD'),('AI', 'AE'),('AI', 'AF'),('AI', 'AH'),('AI', 'J'),
('J', 'AB'),('J', 'C'),('J', 'AD'),('J', 'AF'),('J', 'G'),('J', 'AH'),
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

























#賭けの方向を表している
#かけられた回数をされた回数を紫のノードの大きさで表し、利他行為した回数を赤丸で表している。
import matplotlib.pyplot as plt
import networkx as nx


nodes = ['AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','A','C','D','E','F','G','H','I','J']
#ノードの大きさは利他行為された回数
scores = [0.157480315,0.3149606299,0.9448818898,2.598425197,0.6299212598,2.755905512,0.3149606299,1.338582677,0.6299212598,0.3149606299,0.7894736842,1.842105263,2.236842105,0.3947368421,2.236842105,0.7894736842,0.9210526316,0.3947368421,0.3947368421]
colors = ["#661065" , "#661065" , "#661065" , "#661065" , "#661065" , "#661065" , "#661065" , "#661065" , "#661065" , "#661065"  , "#ff6347" ,   "#ff6347" ,  "#ff6347" ,  "#ff6347" ,  "#ff6347"  ,  "#ff6347" ,  "#ff6347" ,  "#ff6347" ,  "#ff6347" ]
styles = ["filled"] * len(nodes)

pos = {
'AA': (40, 90),
'AB': (60, 90),
'AC': (10, 70),
'AD': (30, 50),
'AE': (10, 30),
'AF': (75, 70),
'AG': (90, 50),
'AH': (80, 40),
'AI': (50, 10),
'AJ': (70, 10),
'A': (40, 90),
'C': (10, 70),
'D': (30, 50),
'E': (10, 30),
'F': (75, 70),
'G': (90, 50),
'H': (80, 40),
'I': (50, 10),
'J': (70, 10)
}

# 各ノードに対応する情報を保存するため辞書として保存
new_nodes = { n : { "score" : scores[i], "pos" : pos[n], "color" : colors[i], "style" : styles[i] ,"size" : 0 } for i, n in enumerate(nodes) }


edges = [
('A', 'C'),('A', 'AD'),('A', 'AE'),('A', 'G'),('A', 'J'),
('AB', 'C'),('AB', 'AF'),('AB', 'AH'),
('C', 'A'),('C', 'AB'),('C', 'AD'),('C', 'AE'),('C', 'AF'),('C', 'G'),
('AD', 'C'),('AD', 'AE'),('AD', 'AF'),('AD', 'G'),('AD', 'AH'),('AD', 'AI'),
('AE', 'AD'),('AE', 'AF'),('AE', 'AH'),('AE', 'AI'),
('AF', 'AB'),('AF', 'AD'),('AF', 'AE'),('AF', 'AH'),('AF', 'AI'),
('G', 'AD'),('G', 'AF'),('G', 'AH'),
('AH', 'A'),('AH', 'C'),('AH', 'AD'),('AH', 'AE'),('AH', 'AF'),('AH', 'AI'),
('AI', 'AD'),('AI', 'AE'),('AI', 'AF'),('AI', 'AH'),('AI', 'J'),
('J', 'AB'),('J', 'C'),('J', 'AD'),('J', 'AF'),('J', 'G'),('J', 'AH'),
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


agraph.draw("network_ritakake2.png", prog="neato", format="png")