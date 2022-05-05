import pandas as pd
import networkx as nx
from sklearn.preprocessing import LabelEncoder
from MeasureNetwrok import MeasureNetwork


def gen_TransNet(score, target, save=False):
    le = LabelEncoder()

    data = pd.read_csv(score)
    length = len(data)

    route = {}
    edges = []
    for item in range(length):
        i = item
        row1 = data.iloc[i, :]
        name1 = row1.line_name
        list1 = row1.station_name
        list1 = list1.split(',')
        list1[0] = list1[0][1:]
        list1[len(list1) - 1] = list1[len(list1) - 1][:-1]
        route[name1] = list1
    keys = list(route)
    le.fit(keys)
    keys_num = le.transform(keys)
    # 获取站点名称与编号之间的对应关系
    mapRes = {}
    for cl in le.classes_:
        mapRes.update({cl: le.transform([cl])[0]})

    for i in range(0, length):
        loc1 = route[keys[i]]
        for j in range(i + 1, length):
            loc2 = route[keys[j]]
            for item in loc1:
                if item in loc2:
                    edges = edges + [(keys_num[i], keys_num[j])]
                    break
    G = nx.Graph(edges)
    if save:
        save_Line_map(mapRes, 'results/LineMap.csv')
        nx.write_gexf(G, target)
    return G


def save_Line_map(inputdata, savepath):
    stationName = inputdata.keys()
    stationNum = inputdata.values()
    newdic = {
        'LineName': stationName,
        'LineNum': stationNum
    }
    res = pd.DataFrame(newdic, columns=['LineNum', 'LineName'])
    res.to_csv(savepath, index=False)


if __name__ == '__main__':
    transNetPath = 'NetworkFiles/qingdao_bus.gexf'
    graph = gen_TransNet('data/bus_no_dupl.csv', transNetPath, True)
    # graph = nx.read_gexf(transNetPath)
    print(graph)
    measure = MeasureNetwork(graph)
    stationName = pd.read_csv('results/LineMap.csv')
    res = pd.merge(measure, stationName, on='LineNum')
    print(res.head())
    res.to_excel('results/MeasureNetwork.xlsx', index=False)



