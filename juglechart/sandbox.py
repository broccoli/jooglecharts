
from juglechart_api import dataframe_to_gviz


import json

import pandas as pd


cities = ['Seattle']
# dates = [dt(2015, 01, 01), dt(2015, 01, 02), dt(2015, 01, 03), dt(2015, 01, 04)]
nums = [45]
# floats = [4.56, 2.6, 7.6, 5.3]
# floats2 = [10.2345, 14.3, 13.532, 11.5554]

df1 = pd.DataFrame({'cities': cities, 'nums': nums}, columns=['cities', 'nums'])

table = dataframe_to_gviz(df1)

j = table.ToJSon()

d = json.loads(j)

print d
d['cols'][1].update({'p': {'role':'interval'}})

j2 = json.dumps(d)

print j2




