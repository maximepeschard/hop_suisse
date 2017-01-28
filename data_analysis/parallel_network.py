
# import useful modules
import pandas as pd
import numpy as np

import itertools as itt
import multiprocessing


# define the pool
pool_size  = multiprocessing.cpu_count()
pool = multiprocessing.Pool(pool_size)
print("we are using, max N thread on cpu=",pool_size) 

# get dataset
full_df = pd.read_pickle('../../df_userID.pickle')
full_df.drop(['MinTemp','MaxTemp','Weather',
              'LivingPlace','Rank','Category','Name',
              'Race','Date','RaceYear','RaceMonth','Place'],axis=1,inplace=True)


# define dict for graph nodes
nodes_dict = dict.fromkeys(full_df.UserID.unique()[:40])

# define global vars for parallel
my_manager = multiprocessing.Manager()
glob_dic = my_manager.dict(nodes_dict)



# define my loop function
def my_loop(c):
    
    c0_races = full_df[full_df.UserID==c[0]].RaceID.unique()
    c1_races = full_df[full_df.UserID==c[1]].RaceID.unique()
    n_shared_race = len(set(c0_races) & set(c1_races))
    
    if n_shared_race!=0:

        return [c[0],c[1],{'weight':n_shared_race}]


# running the parallel loop!
edge_list =  pool.map(my_loop,itt.combinations(nodes_dict.keys(),2))



