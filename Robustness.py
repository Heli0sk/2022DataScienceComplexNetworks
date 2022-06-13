import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


def loadData():
    transNetPath = 'NetworkFiles/qingdao_bus.gexf'
    graph = nx.read_gexf(transNetPath)
    degree = pd.read_excel('results/MeasureNetwork.xlsx', sheet_name='Degree',
                           names=['LineNum', 'Degree'], usecols=[0, 1])
    degree.sort_values('Degree', inplace=True, ascending=False)
    degree = degree['LineNum'].values
    between = pd.read_excel('results/MeasureNetwork.xlsx', sheet_name='Betweenness',
                            names=['LineNum', 'Betweenness'], usecols=[0, 1])
    between.sort_values('Betweenness', inplace=True, ascending=False)
    between = between['LineNum'].values

    return graph, degree, between


#  最大连通子图相对大小
def max_subgraph_size(G):
    if not list(nx.connected_components(G)):
        return 0
    if G.number_of_edges() == 0 or G.number_of_nodes() == 0:
        return 0
    return len(max(nx.connected_components(G), key=len)) / G.number_of_nodes()


#  连通度
def connectivity(G):
    return G.number_of_edges() / ((G.number_of_nodes()*(G.number_of_nodes()-1))/2)


#  网络的效率
def efficiency(G):
    if G.number_of_edges() == 0:
        return 0
    sumeff = 0
    for u in G.nodes():  # 遍历图G的每个点
        path = nx.shortest_path_length(G, source=u)
        # 在网络G中计算从u开始到其他所有节点（注意包含自身）的最短路径长度。如果两个点之间没有路径，那path里也不会存储这个目标节点（省了判断是否has_path的过程）
        for v in path.keys():  # path是一个字典，里面存了所有目的地节点到u的最短路径长度
            if u != v:  # 如果起终点不同才累加计算效率
                sumeff += 1 / path[v]
    result = (2 / (G.number_of_nodes() * (G.number_of_nodes() - 1))) * sumeff  # 计算网络剩余效率
    return result


def cal_Robustness(g, degree):
    N = g.number_of_nodes()
    rmCount = 0
    subSize = []
    eff = []
    rmPer = []
    for node in degree:
        rmCount += 1
        print(rmCount)
        g.remove_node(str(node))
        subSize.append(max_subgraph_size(g))
        eff.append(efficiency(g))
        rmPer.append(rmCount/N)
    return rmPer, subSize, eff


def plot_Robust(rm, sub, eff):
    pass


if __name__ == '__main__':
    graph, degree, between = loadData()
    print(max_subgraph_size(graph))
    print(efficiency(graph))
    # rmPer, subSize, eff = cal_Robustness(graph, degree)
    # data = {
    #         "Remove": rmPer,
    #         "MaxSubgraphSize": subSize,
    #         "Efficiency": eff,
    #     }
    # order = ["Remove", "MaxSubgraphSize", "Efficiency"]
    # pd.DataFrame(data)[order].to_csv('results/Robustness_degree.csv', index=False)
    # print(rmPer, subSize, eff)

    rmPer, subSize, eff = cal_Robustness(graph, between)
    data = {
        "Remove": rmPer,
        "MaxSubgraphSize": subSize,
        "Efficiency": eff,
    }
    order = ["Remove", "MaxSubgraphSize", "Efficiency"]
    pd.DataFrame(data)[order].to_csv('results/Robustness_between.csv', index=False)
    print(rmPer, subSize, eff)
    print(1111)





