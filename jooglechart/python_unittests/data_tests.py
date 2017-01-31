'''
Created on Jan 30, 2017

@author: richd
'''

from jooglechart.data import get_description_from_dataframe, get_description_from_list, _Data

import unittest
from datetime import datetime, date

import pandas as pd

class Test(unittest.TestCase):


    """
    Test get_description_from_dataframe
    """


    def test_gdfdf_string(self):
        fruit = ['apple', 'banana']
         
        df = pd.DataFrame({'fruit': fruit})
        datetime_cols = []
        description = get_description_from_dataframe(df, datetime_cols)
        
        expected = [('0', 'string', 'fruit')]
        self.assertEqual(description, expected)


    def test_gdfdf_int(self):
        ints = [3, 5]
         
        df = pd.DataFrame({'ints': ints})
        datetime_cols = []
        description = get_description_from_dataframe(df, datetime_cols)
        
        expected = [('0', 'number', 'ints')]
        self.assertEqual(description, expected)


    def test_gdfdf_floats(self):
        floats = [3.3, 5.1]
         
        df = pd.DataFrame({'floats': floats})
        datetime_cols = []
        description = get_description_from_dataframe(df, datetime_cols)
        
        expected = [('0', 'number', 'floats')]
        self.assertEqual(description, expected)


    def test_gdfdf_bools(self):
        bools = [False, True]
         
        df = pd.DataFrame({'bools': bools})
        datetime_cols = []
        description = get_description_from_dataframe(df, datetime_cols)
        
        expected = [('0', 'boolean', 'bools')]
        self.assertEqual(description, expected)

    def test_gdfdf_date(self):
        
        dates = [pd.to_datetime("2010-01-20"), pd.to_datetime("2016-04-12")]
         
        df = pd.DataFrame({'dates': dates})
        datetime_cols = []
        description = get_description_from_dataframe(df, datetime_cols)
        
        expected = [('0', 'date', 'dates')]
        self.assertEqual(description, expected)



    """
    test get_description_from_list    
    """
    
    def test_gdfl_string(self):
        
        headers = ['kid', "pet"]
        row1 = ["Jan", "dog"]
        row2 = ["Bobby", "cat"]
        data = [headers, row1, row2 ]
        
        description = get_description_from_list(data)
        
        expected = [('0', 'string', 'kid'), ('1', 'string', 'pet')]
        self.assertEqual(description, expected)

    def test_gdfl_int(self):
        
        headers = ['kid', "pet"]
        row1 = [3, 200]
        row2 = [6, 42]
        data = [headers, row1, row2 ]
        
        description = get_description_from_list(data)
        
        expected = [('0', 'number', 'kid'), ('1', 'number', 'pet')]
        self.assertEqual(description, expected)

    def test_gdfl_float(self):
        
        headers = ['kid', "pet"]
        row1 = [3, 5.6]
        row2 = [6, 10.01]
        data = [headers, row1, row2 ]
        
        description = get_description_from_list(data)
        
        expected = [('0', 'number', 'kid'), ('1', 'number', 'pet')]
        self.assertEqual(description, expected)

    def test_gdfl_boolean(self):
        
        headers = ['kid', "pet"]
        row1 = [3, True]
        row2 = [6, False]
        data = [headers, row1, row2 ]
        
        description = get_description_from_list(data)
        
        expected = [('0', 'number', 'kid'), ('1', 'boolean', 'pet')]
        self.assertEqual(description, expected)


    def test_gdfl_dates(self):
        
        headers = ['kid', "start", "finish"]
        row1 = [3, date(2010, 02, 24), datetime(2011, 12, 10, 5, 2, 3)]
        row2 = [6, date(2013, 02, 24), datetime(2014, 12, 10, 14, 23, 45)]
        data = [headers, row1, row2 ]
        
        description = get_description_from_list(data)
        
        expected = [('0', 'number', 'kid'), ('1', 'date', 'start'), ('2', 'datetime', 'finish')]
        self.assertEqual(description, expected)

    def test_df_to_list(self):
        
        kids = ['Peter', 'Cindy', "Marsha"]
        pets = [2, 1, 3]
        data = {'kids': kids, 'pets': pets}
        
        columns = ['kids', 'pets']
        
        df = pd.DataFrame(data, columns=columns)
        
        obj = _Data(df)
        print "list: " , obj.list
        
        
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()