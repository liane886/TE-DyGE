
import numpy as np
import random
from typing import Tuple
import networkx as nx
import scipy.stats
from numpy.random import choice

class TemporalRandomWalk():

    def __init__(self, nx_G):
        self.G = nx_G

    def sampling_edge(self):
        
        edges = list(self.G.edges(data=True))
        edges = sorted(edges, key = lambda x:x[2].values()[0])
        timestamps = [e[2].values()[0] for e in edges]

        # linear distribution 
        r = scipy.stats.rankdata(timestamps, 'dense')
        probs = r / np.sum(r)
        # Sample edge over distribution
        sampled_t = random.choice(timestamps)
        # sampled_t = choice(timestamps, weights=probs)[0]

        valid_e = [e for e in edges if e[2].values()[0]==sampled_t]
        print('sampled_t',sampled_t)
        print(valid_e)
        # sampled_e = choice(valid_e)[0]
        sampled_e = random.choice(valid_e)

        return sampled_e


    def Walk(self, walk_length):

        start_edges = self.sampling_edge()
        self.walk = [start_edges[:2]]
        t = start_edges[-1].values()[0]
        j = self.walk[-1][0]
        print('t',t)
        print('walk',self.walk)
        print('j',j)
        # Iterates until length of walk is reached 
        for _ in range(walk_length - 2):
            
            # Compute in-between periods of time between source node and temporal neighbors
            cur_nbrs = list(self.G.edges(j,data=True))
            cur_nbrs = sorted(cur_nbrs, key = lambda x:x[2].values()[0])
            # print('cur_nbrs',cur_nbrs)
            timestamps = np.array([e[2].values()[0] for e in cur_nbrs])
            print("timestamps",timestamps)
            valid_times = timestamps[timestamps >= t]
            print("valid_times",valid_times)
            # valid_e = [e for e in edges if e[2].values()[0]==sampled_t]
            # print(c)
            # timesteps = np.array(list())
            # valid_times = timesteps[timesteps >= t]
            delta_times = valid_times - t

            # Compute probability distribution of in-between period of times, according to strategy.
            # Then, sample timestep inl inear distribution 
            # r = scipy.stats.rankdata(delta_times, reverse=True)
            # probs = r / np.sum(r) 
            # # Sampling is temporally biased towards closest time-related neighbors
            # # sampled_t = random.choices(valid_times, weights=probs)[0] <- using distribution
            sampled_t = random.choice(valid_times)

            # Randomly chose (uniform) node in events that occured at sampled time
            # neighbs = self.sg.data.get(j).get(sampled_t)

            # # sampled_n = random.choices(neighbs)[0]    <- using distribution
            # sampled_n = random.choice(neighbs)
            # self.walk.append(sampled_n)

            # # Update current nodes and timestamp
            # j = sampled_n
            t = sampled_t



def load_graphs(dataset_str):
    """Load graph snapshots given the name of dataset"""
    graphs = np.load("../data/{}/{}".format(dataset_str, "graphs.npz"), allow_pickle=True,fix_imports=True)['graph']
    print("Loaded {} graphs ".format(len(graphs)))
    adj_matrices = map(lambda x: nx.adjacency_matrix(x), graphs)
    return graphs, adj_matrices


graphs,_ = load_graphs("Enron_new")
print("Computing training pairs ...")
context_pairs_train = []
k = TemporalRandomWalk(graphs[0])
k.Walk(3)
# for i in range(0):
#     context_pairs_train.append(k.Walk(graphs[i], graphs[i].nodes()))