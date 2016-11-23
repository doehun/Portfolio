from data_generator import data_dictionary_form, data_flat_form, users_db
from get_network import all_networks
import networkx as nx
import numpy as np
import pandas as pd

path = "slack_data/"
users_json_path =  "slack_data/users.json"



from collections import Counter
#Counter(elem[0] for elem in list1)

pairs = []
all = all_networks('slack_data/')

directed = nx.DiGraph()
for i in xrange(len(all)):
    for j in xrange(len(all[i])):
        if j!=0:
            pairs.append((all[i][j], all[i][0]))

c = Counter(p for p in pairs)
keys = c.keys()
keys_directed = c.keys()
values = c.values()


#UNDIRECTED GRAPH = adjacency
adjacency = nx.Graph()
adjacency.add_edges_from(keys)

undirected_graph = nx.to_pandas_dataframe(adjacency)
undirected_graph = undirected_graph.astype(int)


#DIRECTED WEIGHTED GRAPH = directed
for i in xrange(len(keys)):
    keys_directed[i] += (values[i], )

directed.add_weighted_edges_from(keys_directed, weight = 'weight')


#d = nx.to_numpy_matrix(directed)
directed_graph = nx.to_pandas_dataframe(directed)
directed_graph = directed_graph.astype(int)


#To CSV
directed_graph.to_csv("directed_graph.csv")
undirected_graph.to_csv("undirected_graph.csv")



#Pickling
import pickle

pickle_out = open("graphs.picke", "wb")
pickle.dump(directed_graph, pickle_out)
pickle.dump(undirected_graph, pickle_out)
pickle_out.close()

pickle_in = open("graphs.picke", "rb")
first_graph = pickle.load(pickle_in)
second_graph = pickle.load(pickle_in)
print second_graph.head()


#print df.ix["U1L6YQUSU"]

#d.tofile("foo.csv", sep=",",format='%1.0f')
#write_dot(G,'file.dot')
"""
dictionary form of data
"""

#data = data_dictionary_form(path)

#for k, v in data.items():
#    print("\n" + k + "\n")
#    print(v.head())

#print data['general'][700][3]


"""
flat form of data (list of lists)

df = pd.DataFrame(no_users_info_data)
print df.head(10)
users = users_db(users_json_path)
data = no_users_info_data.merge(users, on = 'id', how = 'left')


"""

#List of lists
#data = pd.read_csv("concatenated.csv", header = 0, index = False)

#users = users_db(users_json_path)['id'].unique()
#print len(users)
#raw_data = all_networks(path)
#users = []
#for l in raw_data:
#    users.extend(l)

#print len(set(users))