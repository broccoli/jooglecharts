'''
Created on Jan 9, 2016

@author: richd
'''

import random 
import pandas as pd

import numpy as np


x = ['a', 'b', 'c', 'd']
y = [4, 2, 5, 3]
d = {'x': x, 'y': y}
test_df = pd.DataFrame(d)


def get_random_int():

    pass

def sample_date_sequence(periods):
    
    rng = pd.date_range('1/1/2015', periods=periods, freq='D')

    return rng


def get_random_date_data(days=4, num_series=4):

    data = {}
    data['dates'] = sample_date_sequence(days)
    label_num = 65 # ascii 'A'
    
    for num in range(num_series):
        
        label = chr(label_num)
        mu = random.randint(20, 51)
        sd = 2
        s = np.random.normal(mu, sd, days)
        data[label] = s

        
    return pd.DataFrame(data)


print get_random_date_data(10)

