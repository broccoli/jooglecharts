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


capitals = ['Sacramento', 'Montpelier', 'Juneau', 'Montgomery', 'Little Rock',
              'Phoenix', 'Denver', 'Hartford', 'Tallahassee', 'Dover', 'Atlanta', 'Honolulu',
           'Austin', 'Albany', 'Frankfurt', 'Topeka', 'Baton Rouge']

def get_df(rows=5, cols=1, min=20, max=100, category_column=False):
    random.seed(2)
    cities = capitals[:rows]
    d = {}
    columns = []
    d['cities'] = cities
    columns.append('cities')
    if category_column:
        categories = [chr(random.randint(65, 67)) for x in range(rows)]
        d['categories'] = categories
        columns.append('categories')
        
    for x in range(cols):
        name = chr(x + 65) + (chr(x + 97) * 8) # + chr(x + 97)
        data = [random.randint(min, max) for i in range(rows)]
        d[name] = data
        columns.append(name)
    return pd.DataFrame(d, columns=columns)
