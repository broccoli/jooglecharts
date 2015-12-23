'''
Created on Dec 5, 2015

@author: richd
'''

from juglechart_api import JugleChart, Formatter, Filter, create_nested_dict_from_dotted_key, ChartRow

import gviz_api


import json

import pandas as pd
from datetime import datetime as dt

data = [
        ['Year', 'Visitations'],
        ['2010', 10],
        ['2010', 14],
        ['2020', 16],
        ['2040', 22],
        ['2040', 28]
      ]

# Creating the data
description = [("Year", "string"), ("Visitations", "number")]
data2 = [
        ['2010', 10],
        ['2010', 14],
        ['2020', 16],
        ['2040', 22],
        ['2040', 28]
          ]



data_table = gviz_api.DataTable(description)
data_table.LoadData(data2)





cities = ['Seattle', 'Chicago', 'Phoenix', 'Atlanta']
dates = [dt(2015, 01, 01), dt(2015, 01, 02), dt(2015, 01, 03), dt(2015, 01, 04)]
nums = [45, 74, 33, 50]
floats = [4.56, 2.6, 7.6, 5.3]
floats2 = [10.2345, 14.3, 13.532, 11.5554]

df1 = pd.DataFrame({'cities': cities, 'nums': nums}, columns=['cities', 'nums'])
# df2= pd.DataFrame({'dates': dates, 'nums': nums}, columns=['dates', 'nums'])
df3= pd.DataFrame({'dates': dates, 'floats': floats, 'floats2':floats2}, columns=['dates', 'floats', 'floats2'])


list1 = []
list1.append(['Cat1', 'Cat2', 'count'])
list1.append(['1', 'a', 34])
list1.append(['1', 'b', 23])
list1.append(['1', 'k', 84])
list1.append(['2', 'a', 62])
list1.append(['2', 'm', 46])
list1.append(['2', 'c', 68])
list1.append(['3', 'g', 24])
list1.append(['3', 'b', 86])
list1.append(['3', 'c', 45])



# gchart = JugleChart(list1)

gchart = JugleChart(df1)
# gchart = JugleChart(df3['dates'], df3['floats'])

# gchart.chart_type = "TableChart"


# print df3
# gchart = JugleChart(df1)

gchart.add_chart_options(hAxis_title="QWERT", hAxis_textStyle_color="#FF0000")

# gchart.add_div_styles(height="400px", width="600px")

c1 = gchart
c2 = c1.copy()
c2.chart_type = "PieChart"
c2.add_chart_options(title="This is a PieChart")
c1.add_chart_options(title="This is a ColumnChart")


filter1 = Filter(type="NumberRangeFilter")
filter1.add_options(filterColumnLabel="nums")
c2.add_filter(filter1)

row = ChartRow(c1, c2)

print row.render()




# filter1 = Filter(type="CategoryFilter")
# filter1.add_options(filterColumnIndex=0, ui_allowMultiple=True, ui_allowNone=True)
# gchart.add_filter(filter1)
# 
# 
# filter2 = Filter(type="CategoryFilter")
# filter2.add_options(filterColumnIndex=1, ui_allowMultiple=True, ui_allowNone=True)
# gchart.add_filter(filter2)
# 
# # print filter2.filter_name
# filter1.bind_filter(filter2)


# filter1.add_options(a_b_c=3)
# print filter1.render()



# money_format = {'prefix':'$', 'fractionDigits': 2}
# gchart.add_formatter('number', options=money_format, cols=[1, 2])
# gchart.add_formatter('number', options=money_format, cols=[3])

# pattern = "------ {0} ====== {1} ------"
# gchart.add_formatter('pattern', pattern=pattern, source_cols=[1, 2])

# f1 = Formatter(type='NumberFormat', options = money_format, cols=[0])
# f2 = Formatter(type='NumberFormat', options = money_format, cols=[0])

# print f1.render()
# print f2.render()

# gchart.hide_cols = [0]
# print gchart.render('Table')

