import re
import networkx as nx
from pylab import *
import numpy as np
import pandas as pd

# 1.数据导入
qingdao_data = pd.read_csv('data/qingdao2.csv')
# print(qingdao_data.columns.values.tolist())
# ['line', 'line_name', 'line_path', 'station_location', 'station_name']
# 2.数据处理，station存储的是公交网络的所有站点信息
station = []
for i in qingdao_data['station_name']:
    i = re.sub('[[]', '', i)
    i = re.sub('[]]', '', i)
    i = re.sub('[\']', '', i)
    list1 = i.split(',')
    for j in list1:
        if j not in station:
            station.append(j)

# 3.将每个站点经过的公交路线进行存储
line = qingdao_data['line_name']
# print(line[1])

# 当前需要处理的是按照站点来寻找经过某一站点的所有线路
length = len(line)
relationship = np.zeros((length, length))

for i in station:
    list1 = []
    for j in range(len(qingdao_data)):
        if i in qingdao_data['station_name'][j]:
            list1.append(j)
    for k in list1:
        for w in list1:
            if k != w:
                relationship[k][w] = 1

G = nx.Graph()  # 初始化
# G = nx.Graph(name='my graph')
for i in range(len(line)):
    G.add_node(i)

for i in range(len(qingdao_data['line_name'])):
    for j in range(len(qingdao_data['line_name'])):
        if (relationship[i][j] == 1):
            G.add_edge(i, j)
        # print(i,end=',')
        # print(j)
# G.add_edges_from(relationships)

nx.write_gexf(G, 'data/qingdao2.gexf')
