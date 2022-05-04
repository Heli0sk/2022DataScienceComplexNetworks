import pandas as pd
import networkx as nx
from sklearn.preprocessing import LabelEncoder


def gen_TransNet(score, target):
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
    nx.write_gexf(G, target)


if __name__ == '__main__':
    transNetPath = 'NetworkFiles/qingdao_bus.gexf'
    gen_TransNet('data/bus_no_dupl.csv', transNetPath)


