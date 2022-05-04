import networkx as nx
import pandas as pd


def MeasureNetwork(graph):
    dgr = nx.degree_centrality(graph)
    clo = nx.closeness_centrality(graph)
    har = nx.harmonic_centrality(graph)
    eig = nx.eigenvector_centrality(graph)
    bet = nx.betweenness_centrality(graph)
    pgr = nx.pagerank(graph)
    hits = nx.hits(graph)
    centralities = pd.concat(
        [pd.Series(c) for c in (hits[1], eig, pgr, har, clo, hits[0], dgr, bet)],
        axis=1)

    centralities.columns = ("Authorities", "Eigenvector", "PageRank",
                            "Harmonic Closeness", "Closeness", "Hubs",
                            "Degree", "Betweenness")
    centralities["Harmonic Closeness"] /= centralities.shape[0]

    return centralities