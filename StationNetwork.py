import pandas as pd
import networkx as nx
from sklearn.preprocessing import LabelEncoder
from MeasureNetwrok import MeasureNetwork


def gen_StationNet(score, target, save=False):
    data = pd.read_csv(score)
    stationNames = data.station_name.values
    allStations = []
    for item in stationNames:
        stations = item.split(',')
        stations[0] = stations[0][1:]
        stations[len(stations) - 1] = stations[len(stations) - 1][:-1]
        allStations += stations

    edges = []
    le = LabelEncoder()
    le.fit(allStations)
    keys_num = le.transform(allStations)
    # 获取站点名称与编号之间的对应关系
    mapRes = {}
    for cl in le.classes_:
        mapRes.update({cl: le.transform([cl])[0]})

    stationName = mapRes.keys()
    stationNum = mapRes.values()
    newdic = {
        'StationName': stationName,
        'StationNum': stationNum
    }
    res = pd.DataFrame(newdic, columns=['StationNum', 'StationName'])
    res.to_csv('results/StationMap.csv', index=False)

    for i in range(1, len(keys_num)):
        # if [keys_num[i], keys_num[i-1]] not in edges:
        edges += [(keys_num[i], keys_num[i-1])]
    G = nx.Graph(edges)
    if save:
        # save_Line_map(mapRes, 'results/StationMap.csv')
        nx.write_gexf(G, target)
    return G


if __name__ == '__main__':
    transNetPath = 'NetworkFiles/stationGraph.gexf'
    graph = gen_StationNet('data/bus_no_dupl.csv', transNetPath, True)
    # graph = nx.read_gexf(transNetPath)
    print(graph)
    # measure = MeasureNetwork(graph)
    # stationName = pd.read_csv('results/LineMap.csv')
    # res = pd.merge(measure, stationName, on='LineNum')
    # print(res.head())
    # res.to_excel('results/MeasureNetwork.xlsx', index=False)



