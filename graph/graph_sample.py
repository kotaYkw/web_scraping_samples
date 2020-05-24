import pygraphviz as pgv
import networkx as nx

G = nx.Graph()

# 小文字の label にすれば Graphviz 側でラベルとして認識される
# Gephi 側では大文字・小文字どちらでもOK
G.add_edges_from([('ノード1', 'ノード2', {'label': 'エッジ', 'weight': 0.2})])
print(list(G.nodes))

# 属性を追加することも可能
G.nodes['ノード1']['style'] = 'solid,filled'
G.nodes['ノード1']['fillcolor'] = '#ccccff'
G.nodes['ノード1']['shape'] = 'egg'

G.nodes['ノード2']['color'] = '#ff9999'
G.nodes['ノード2']['fontcolor'] = 'red'

G.edges['ノード1', 'ノード2']['style'] = 'dotted'
G.edges['ノード1', 'ノード2']['fontsize'] = 10
G.edges['ノード1', 'ノード2']['fontcolor'] = '#00cc66'

nx.write_graphml(G, "test.graphml")  # Gephi 用に GraphML ファイルを出力

# GraphViz用にAGraphへ変換して描画
ag = nx.nx_agraph.to_agraph(G)
ag.node_attr.update(fontname="MS Gothic")  # Windowsで MS Gothic を使う場合
ag.edge_attr.update(fontname="MS Gothic")
print(ag)  # dot言語で確認できる
#ag.draw('test.pdf', prog='fdp')  # レイアウトは fdp を指定してみます
