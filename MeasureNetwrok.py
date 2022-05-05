import networkx as nx
import pandas as pd


def get_degree(data):
    d = nx.degree(data)
    node = []
    degree = []
    for item in d:
        node.append(item[0])
        degree.append(item[1])
    res = {k: v for k, v in zip(node, degree)}
    return res, node


def MeasureNetwork(graph, save=False):
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

    centralities.columns = ("stationNum", "Degree", "Clustering", "Eigenvector", "PageRank", "Closeness",
                            "Degree_C", "Betweenness")
    # centralities["Harmonic Closeness"] /= centralities.shape[0]
    centralities['stationNum'] = centralities['stationNum'].apply(pd.to_numeric, errors='coerce')
    res = centralities.sort_values('stationNum', ascending=True)

    stationName = pd.read_csv('data/stationMap.csv')
    res = pd.merge(res, stationName, on='stationNum')

    if save:
        res.to_excel('results/MeasureNetwork.xlsx', index=False)
    return res


if __name__ == '__main__':
    transNetPath = 'NetworkFiles/qingdao_bus.gexf'
    graph = nx.read_gexf(transNetPath)
    print(graph)
    mea = MeasureNetwork(graph, True)
    print(mea.head())

