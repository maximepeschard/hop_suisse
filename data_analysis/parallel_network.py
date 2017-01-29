
# import useful modules
import pandas as pd
import numpy as np

import itertools as itt
import multiprocessing
import networkx as nx


# get and clean dataset
full_df = pd.read_pickle('../../df_userID.pickle')
full_df.drop(['MinTemp','MaxTemp','Weather',
              'LivingPlace','Rank','Category','Name',
              'Race','Date','RaceYear','RaceMonth','Place'],axis=1,inplace=True)

# select enthusiasts :) !!
single_events_counts = full_df.UserID.value_counts()
enthusiasts = [k for k,v in single_events_counts.items() if v>70]

# define dict for graph nodes
# nodes_dict = dict.fromkeys(full_df.UserID.unique()[:20])
nodes_dict = dict.fromkeys(enthusiasts)


# define global vars for parallel
# my_manager = multiprocessing.Manager()
# glob_dic = my_manager.dict(nodes_dict)

# define graph
# runner_graph = nx.Graph() # define graph
# runner_graph.add_nodes_from(nodes_dict.keys()) # add nodes

# custom function to add edges and weights
def my_loop(c):
    
    c0_races = full_df[full_df.UserID==c[0]].RaceID.unique()
    c1_races = full_df[full_df.UserID==c[1]].RaceID.unique()
    n_shared_race = len(set(c0_races) & set(c1_races))
    
    if n_shared_race!=0:

        # add diredctly the edge on the graph
        # runner_graph.add_edge(c[0],c[1],weight = n_shared_race)

        return (c[0],c[1],{'weight':n_shared_race})

if __name__ == '__main__':

	# define the pool
	pool_size  = multiprocessing.cpu_count()
	pool = multiprocessing.Pool(pool_size)
	print("we are using, max N threads on cpu =",pool_size) 

	# running the parallel loop!
	edge_list =  pool.map(my_loop,itt.combinations(nodes_dict.keys(),2))

# save edge_list
import pickle
with open('outfile.txt', 'wb') as fp:
    pickle.dump(edge_list, fp)

# save the GRAPH!
# nx.write_gpickle(runner_graph,'runner_graph')
