import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_degree(data):
    d = nx.degree(data)
    node = []
    degree = []
    for item in d:
        node.append(item[0])
        degree.append(item[1])
    res = {k: v for k, v in zip(node, degree)}
    return res, node


def MeasureNetwork(graph):
    degree, node = get_degree(graph)
    dgr = nx.degree_centrality(graph)
    cluster = nx.clustering(graph)
    clo = nx.closeness_centrality(graph)
    # har = nx.harmonic_centrality(graph)
    eig = nx.eigenvector_centrality(graph)
    bet = nx.betweenness_centrality(graph)
    pgr = nx.pagerank(graph)
    nodes = {k: v for k, v in zip(node, node)}

    centralities = pd.concat(
        [pd.Series(c) for c in (nodes, degree, cluster, eig, pgr, clo, dgr, bet)],
        axis=1)

    centralities.columns = ("LineNum", "Degree", "Clustering", "Eigenvector", "PageRank", "Closeness",
                            "Degree_C", "Betweenness")
    # centralities["Harmonic Closeness"] /= centralities.shape[0]
    centralities['LineNum'] = centralities['LineNum'].apply(pd.to_numeric, errors='coerce')
    res = centralities.sort_values('LineNum', ascending=True)

    # stationName = pd.read_csv('data/LineMap.csv')
    # res = pd.merge(res, stationName, on='LineNum')

    # if save:
    #     res.to_excel('results/MeasureNetwork.xlsx', index=False)
    return res


def degreeDistribution(datapath, savepath, save=False):
    def normfun(x, mu, sigma):
        pdf = np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (sigma * np.sqrt(2 * np.pi))
        return pdf

    measure = pd.read_excel(datapath)

    lst = measure['Degree'].values.tolist()
    res = dict(zip(*np.unique(lst, return_counts=True)))

    x = np.unique(lst, return_counts=True)[0]
    y = np.unique(lst, return_counts=True)[1]

    mean = y.mean()
    std = x.std()
    y_ = normfun(x, mean, std)
    bias = 1000
    plt.plot(x, y_ * bias, color='red')
    plt.bar(x, y, color='blue')

    # 设置图表参数
    plt.xlabel('Degreee', fontsize=15, color='black')  # 设置x轴标签
    plt.ylabel('Frequency', fontsize=15, color='black')  # 设置y轴标签

    if save:
        plt.savefig(savepath)
    plt.show()


if __name__ == '__main__':
    transNetPath = 'NetworkFiles/qingdao_bus.gexf'
    graph = nx.read_gexf(transNetPath)
    print(graph)
    mea = MeasureNetwork(graph)
    print(mea.head())

