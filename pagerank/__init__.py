import numpy as np
import random
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
# %matplotlib inline
plt.rcParams['font.sans-serif']=['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False  # 用来正常显示负号\

if __name__ == '__main__':
    df = pd.read_csv('triples.csv')
    print(df)

    edges = [edge for edge in zip(df['head'], df['tail'])]
    G = nx.DiGraph()
    G.add_edges_from(edges)
    plt.figure(figsize=(15, 14))
    pos = nx.spring_layout(G, iterations=3, seed=5)
    nx.draw(G, pos, with_labels=True)
    plt.show()

    pagerank = nx.pagerank(G,  # NetworkX graph 有向图，如果是无向图则自动转为双向有向图
                           alpha=0.85,  # Damping Factor
                           personalization=None,  # 是否开启Personalized PageRank，随机传送至指定节点集合的概率更高或更低
                           max_iter=100,  # 最大迭代次数
                           tol=1e-06,  # 判定收敛的误差
                           nstart=None,  # 每个节点初始PageRank值
                           dangling=None,  # Dead End死胡同节点
                           )
    print(sorted(pagerank.items(), key=lambda x: x[1], reverse=True))

    # 节点颜色
    M = G.number_of_edges()
    edge_colors = range(2, M + 2)

    plt.figure(figsize=(15, 14))
    # 节点尺寸
    node_sizes = (np.array(list(pagerank.values())) * 8000).astype(int)
    # 绘制节点
    nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_sizes)

    # 绘制连接
    edges = nx.draw_networkx_edges(
        G,
        pos,
        node_size=node_sizes,  # 节点尺寸
        arrowstyle="->",  # 箭头样式
        arrowsize=20,  # 箭头尺寸
        edge_color=edge_colors,  # 连接颜色
        edge_cmap=plt.cm.plasma,  # 连接配色方案，可选：plt.cm.Blues
        width=4  # 连接线宽
    )

    # 设置每个连接的透明度
    edge_alphas = [(5 + i) / (M + 4) for i in range(M)]
    for i in range(M):
        edges[i].set_alpha(edge_alphas[i])

    # # 图例
    # pc = mpl.collections.PatchCollection(edges, cmap=cmap)
    # pc.set_array(edge_colors)
    # plt.colorbar(pc)

    ax = plt.gca()
    ax.set_axis_off()
    plt.show()