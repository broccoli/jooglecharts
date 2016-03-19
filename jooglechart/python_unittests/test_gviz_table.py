'''
Created on Dec 6, 2015

@author: richd
'''
import unittest

from pandas import DataFrame
import pandas as pd
import numpy as np

from jooglechart.jooglechart_api import dataframe_to_gviz, JoogleChartsException

from datetime import datetime, date

class Test(unittest.TestCase):
    
    """
    Notes on nulls:
    -- Python None is converted to js null by the gviz_api.
    -- When there is a null in the data, the JSCode just doesn't set that Cell.
       But there is a null in the ToJSon() output.
    -- Adding a NaN to a dataframe for ints makes them floats.
    """


    def test_string(self):
        df = DataFrame({'fruit': ['apple', 'banana']} )
        table = dataframe_to_gviz(df)
#         print table.ToJSCode('data')
        
        expected = """var data = new google.visualization.DataTable();
data.addColumn("string", "fruit", "fruit");
data.addRows(2);
data.setCell(0, 0, "apple");
data.setCell(1, 0, "banana");
"""
        self.assertEqual(table.ToJSCode("data"), expected)
        
    def test_int(self):
        
        df = DataFrame({'nums': [5, 1000]} )
        table = dataframe_to_gviz(df)
#         print table.ToJSCode('data')
        
        expected = """var data = new google.visualization.DataTable();
data.addColumn("number", "nums", "nums");
data.addRows(2);
data.setCell(0, 0, 5);
data.setCell(1, 0, 1000);
"""
        self.assertEqual(table.ToJSCode("data"), expected)
        
    def test_float(self):
        
        df = DataFrame({'floats': [5, 3.456]} )
        table = dataframe_to_gviz(df)
#         print table.ToJSCode('data')

        expected = """var data = new google.visualization.DataTable();
data.addColumn("number", "floats", "floats");
data.addRows(2);
data.setCell(0, 0, 5.0);
data.setCell(1, 0, 3.456);
"""
        self.assertEqual(table.ToJSCode("data"), expected)
        

    def test_boolean(self):
        
        df = DataFrame({'booleans': [True, False]} )
        table = dataframe_to_gviz(df)
#         print table.ToJSCode('data')

        expected = """var data = new google.visualization.DataTable();
data.addColumn("boolean", "booleans", "booleans");
data.addRows(2);
data.setCell(0, 0, true);
data.setCell(1, 0, false);
"""
        self.assertEqual(table.ToJSCode("data"), expected)
        

    def test_date_001(self):
        
        # datetime with y, m, d
        
        df = DataFrame({'dates': [datetime(2015, 03, 21), datetime(1999, 12, 01 )]} )
        table = dataframe_to_gviz(df)
#         print table.ToJSCode('data')

        expected = """var data = new google.visualization.DataTable();
data.addColumn("date", "dates", "dates");
data.addRows(2);
data.setCell(0, 0, new Date(2015,2,21));
data.setCell(1, 0, new Date(1999,11,1));
"""
        self.assertEqual(table.ToJSCode("data"), expected)
        
    def test_date_002(self):
        
        # datetime with y, m, d, h, m, s
        
        df = DataFrame({'dates': [datetime(2015, 03, 21, 15, 59, 45), datetime(1999, 12, 01, 4, 15, 21)]} )
        table = dataframe_to_gviz(df)
#         print table.ToJSCode('data')

        expected = """var data = new google.visualization.DataTable();
data.addColumn("date", "dates", "dates");
data.addRows(2);
data.setCell(0, 0, new Date(2015,2,21));
data.setCell(1, 0, new Date(1999,11,1));
"""
        self.assertEqual(table.ToJSCode("data"), expected)
        
        
    def test_date_003(self):
        
        # datetime with y, m, d, h, m, s

        df = DataFrame({'dates': [datetime(2015, 03, 21, 15, 59, 45), datetime(1999, 12, 01, 4, 15, 21)]} )
        table = dataframe_to_gviz(df, datetime_cols = [0, 1])
#         print table.ToJSCode('data')

        expected = """var data = new google.visualization.DataTable();
data.addColumn("datetime", "dates", "dates");
data.addRows(2);
data.setCell(0, 0, new Date(2015,2,21,15,59,45));
data.setCell(1, 0, new Date(1999,11,1,4,15,21));
"""
        self.assertEqual(table.ToJSCode("data"), expected)


    def test_date_004(self):
        
        # pandas Timestamp dates
        
        df = DataFrame({'dates': [pd.to_datetime('2015-10-04'), pd.to_datetime('1999-03-21')]} )
        table = dataframe_to_gviz(df)
#         print table.ToJSCode('data')

        expected = """var data = new google.visualization.DataTable();
data.addColumn("date", "dates", "dates");
data.addRows(2);
data.setCell(0, 0, new Date(2015,9,4));
data.setCell(1, 0, new Date(1999,2,21));
"""
        self.assertEqual(table.ToJSCode("data"), expected)


    def test_date_005(self):
        
        # date() with y, m, d
        
        ##### NOTE:  datetime.date() IS TREATED AS A STRING IN PANDAS ######
        
        df = DataFrame({'dates': [date(2015, 03, 21), date(1999, 12, 01 )]} )
        table = dataframe_to_gviz(df)
#         print table.ToJSCode('data')

        expected = """var data = new google.visualization.DataTable();
data.addColumn("string", "dates", "dates");
data.addRows(2);
data.setCell(0, 0, "2015-03-21");
data.setCell(1, 0, "1999-12-01");
"""
        self.assertEqual(table.ToJSCode("data"), expected)
        


    def test_null_001(self):
        
        """ test nan """
        df = DataFrame({'nums': [3,np.nan, 5]})
#         table = dataframe_to_gviz(df)

        self.assertRaises(JoogleChartsException, dataframe_to_gviz, df)


    def test_null_002(self):
        
        """ test nan """
        df = DataFrame({'nums': [3,np.nan, 5]})
        table = dataframe_to_gviz(df, allow_nulls=True)
#         print table.ToJSCode('data')

        expected = """var data = new google.visualization.DataTable();
data.addColumn("number", "nums", "nums");
data.addRows(3);
data.setCell(0, 0, 3.0);
data.setCell(2, 0, 5.0);
"""
        self.assertEqual(table.ToJSCode("data"), expected)


    def test_null_003(self):
        
        """ test NaT """
        df = DataFrame({'dates': [datetime(2015, 03, 21), pd.NaT, datetime(1999, 12, 01 )]} )
#         table = dataframe_to_gviz(df)

        self.assertRaises(JoogleChartsException, dataframe_to_gviz, df)


    def test_null_004(self):
        
        """ test NaT """
        df = DataFrame({'dates': [datetime(2015, 03, 21), pd.NaT, datetime(1999, 12, 01 )]} )
        table = dataframe_to_gviz(df, allow_nulls=True)
#         print table.ToJSCode('data')

        expected = """var data = new google.visualization.DataTable();
data.addColumn("date", "dates", "dates");
data.addRows(3);
data.setCell(0, 0, new Date(2015,2,21));
data.setCell(2, 0, new Date(1999,11,1));
"""
        self.assertEqual(table.ToJSCode("data"), expected)



    def test_null_005(self):
        
        """ test None """
        df = DataFrame({'fruit': ['apple', None, 'plum']})
#         table = dataframe_to_gviz(df)

        self.assertRaises(JoogleChartsException, dataframe_to_gviz, df)


    def test_null_006(self):
        
        """ test None """
        df = DataFrame({'fruit': ['apple', None, 'plum']})
        table = dataframe_to_gviz(df, allow_nulls=True)
#         print table.ToJSCode('data')

        expected = """var data = new google.visualization.DataTable();
data.addColumn("string", "fruit", "fruit");
data.addRows(3);
data.setCell(0, 0, "apple");
data.setCell(2, 0, "plum");
"""
        self.assertEqual(table.ToJSCode("data"), expected)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()