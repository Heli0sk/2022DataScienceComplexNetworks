import pandas as pd
import numpy as np
import networkx as nx
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()

QD = pd.read_csv('data/bus_no_dupl.csv')
length = len(QD)

route = {}
edges = []
for item in range(length):
    i = item
    row1 = QD.iloc[i, :]
    name1 = row1.line_name
    list1 = row1.station_name
    list1 = list1.split(',')
    list1[0] = list1[0][1:]
    list1[len(list1) - 1] = list1[len(list1) - 1][:-1]
    route[name1] = list1
keys = list(route)
le.fit(keys)
keys_num = le.transform(keys)
for i in range(0, length - 1):
    loc1 = route[keys[i]]
    for j in range(i + 1, length):
        loc2 = route[keys[j]]
        for item in loc1:
            if item in loc2:
                edges = edges + [(keys_num[i], keys_num[j])]
                break
G = nx.Graph(edges)
nx.write_gexf(G, 'data/qingdao_bus.gexf')
