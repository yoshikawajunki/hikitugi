#利他行為の方向
#利他行為された回数を青丸のノードの大きさで表し、利他行為した回数を赤丸で表している。
import matplotlib.pyplot as plt
import networkx as nx


nodes = ['A','C','D','E','F','G','H','I','J','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ',]
#ノードの大きさは利他行為された回数
scores = [0.7894736842,1.842105263,2.236842105,0.3947368421,2.236842105,0.7894736842,0.9210526316,0.3947368421,0.3947368421,0.3947368421,0.1315789474,0.6578947368,2.368421053,1.578947368,2.236842105,0.6578947368,1.052631579,0.3947368421,0.5263157895]
colors = ["#ff6347" , "#ff6347" ,  "#ff6347" ,  "#ff6347" ,  "#ff6347" ,  "#ff6347" ,  "#ff6347" ,  "#ff6347" ,  "#ff6347" ,"#ccddff" , "#ccddff" , "#ccddff" , "#ccddff" , "#ccddff" ,  "#ff6347" , "#ccddff" , "#ccddff" ,  "#ff6347" , "#ccddff"  ]
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
('A', 'AB'),('A', 'C'),('A', 'H'),
('C', 'A'),('C', 'AE'),('C', 'AH'),
('AD', 'AE'),('AD', 'F'),('AD', 'G'),('AD', 'AH'),('AD', 'AI'),('D', 'AJ'),
('AE', 'C'),('AE', 'AD'),
('F', 'AD'),('F', 'G'),('F', 'AH'),('F', 'AI'),('F', 'AJ'),
('G', 'AD'),('G', 'AE'),('G', 'F'),('G', 'AH'),('G', 'AJ'),
('AH', 'AD'),('AH', 'F'),('AH', 'AJ'),
('AI', 'F'),
('AJ', 'F'),('AJ', 'G'),('AJ', 'AH')
]


width = [1,4,1,3,10,1,1,9,3,2,1,1,1,2,12,1,1,2,1,1,1,1,2,1,3,3,1,3,1,1,1]
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


agraph.draw("network_ritasizea.png", prog="neato", format="png")

























#利他行為の方向
#利他行為された回数を青丸のノードの大きさで表し、利他行為した回数を赤丸で表している。
import matplotlib.pyplot as plt
import networkx as nx


nodes = ['AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','A','C','D','E','F','G','H','I','J']
#ノードの大きさは利他行為された回数
scores = [0.3947368421,0.1315789474,0.6578947368,2.368421053,1.578947368,2.236842105,0.6578947368,1.052631579,0.3947368421,0.5263157895,0.7894736842,1.842105263,2.236842105,0.3947368421,2.236842105,0.7894736842,0.9210526316,0.3947368421,0.3947368421]
colors = ["#ccddff" , "#ccddff" , "#ccddff" , "#ccddff" , "#ccddff" , "#ccddff" , "#ccddff" , "#ccddff" , "#ccddff" , "#ccddff"  , "#ff6347" ,   "#ff6347" ,  "#ff6347" ,  "#ff6347" ,  "#ccddff"  ,  "#ff6347" ,  "#ff6347" ,  "#ccddff" ,  "#ff6347" ]
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
('A', 'AB'),('A', 'C'),('A', 'H'),
('C', 'A'),('C', 'AE'),('C', 'AH'),
('AD', 'AE'),('AD', 'F'),('AD', 'G'),('AD', 'AH'),('AD', 'AI'),('D', 'AJ'),
('AE', 'C'),('AE', 'AD'),
('F', 'AD'),('F', 'G'),('F', 'AH'),('F', 'AI'),('F', 'AJ'),
('G', 'AD'),('G', 'AE'),('G', 'F'),('G', 'AH'),('G', 'AJ'),
('AH', 'AD'),('AH', 'F'),('AH', 'AJ'),
('AI', 'F'),
('AJ', 'F'),('AJ', 'G'),('AJ', 'AH')
]


width = [1,4,1,3,10,1,1,9,3,2,1,1,1,2,12,1,1,2,1,1,1,1,2,1,3,3,1,3,1,1,1]
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


agraph.draw("network_ritasize.png", prog="neato", format="png")