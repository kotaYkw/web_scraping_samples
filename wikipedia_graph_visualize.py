import networkx
import matplotlib
import matplotlib.pyplot as plt
import dataset
matplotlib.use('Agg')

db = dataset.connect('sqlite:///wikipedia_graph.db')
G = networkx.DiGraph()

print('Building graph...')
for page in db['pages'].all():
	G.add_node(page['url'], title=page['title'])

for link in db['links'].all():
	# 両方のエンドポイントが訪問済みならaddedgeのみ
	if G.has_node(link['from_url']) and G.has_node(link['to_url']):
		G.add_edge(link['from_url'], link['to_url'])

# 未接続のノードを削除
G.remove_nodes_from(networkx.isolates(G))

# ノードの媒介中心性を重要度の尺度として計算する
print('Calculateing betweenness...')
betweenness = networkx.betweenness_centrality(G, endpoints=False)

print('Drawing graph...')

# Sigmoid関数で色を目立つようにする
squish = lambda x : 1 / (1+0.5**(20*(x-0.1)))

colors = [(0, 0, squish(betweenness[n])) for n in G.nodes()]
labels = dict((n, d['title']) for n, d in G.nodes(data=True))
positions = networkx.spring_layout(G)

networkx.draw(G, positions, node_color=colors, edge_color='#AEAEAE')

# 手動でラベルを書いてノードの上に表示させる
for k, v, in positions.items():
	plt.text(v[0], v[1]+0.025, s=labels[k], horizontalalignment='center', size=8)

plt.savefig('wilipedia_graps.png')
