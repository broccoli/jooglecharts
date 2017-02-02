'''
Created on Jan 30, 2017

@author: richd
'''

from jooglechart.data import get_description_from_dataframe, get_description_from_list, _Data, get_list_from_dataframe
from jooglechart.utils import JoogleChartsException

import unittest
from datetime import datetime, date

import pandas as pd
import numpy as np

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


    """
    test get_list_from_dataframe
    """
    def test_df_to_list_1(self):
        
        # normal data
        kids = ['Peter', 'Cindy', "Marsha"]
        pets = [2, 1, 3]
        data = {'kids': kids, 'pets': pets}
        columns = ['kids', 'pets']
        df = pd.DataFrame(data, columns=columns)
        
        list1 = get_list_from_dataframe(df, allow_nulls=True)
#         obj = _Data(df)
        expected = [['Peter', 2], ['Cindy', 1], ['Marsha', 3]]

        self.assertEqual(list1, expected)

    def test_df_to_list_2(self):
        
        # None, without allow_nulls
        kids = ['Peter', 'Cindy', "Marsha"]
        pets = [2, 1, None]
        data = {'kids': kids, 'pets': pets}
        columns = ['kids', 'pets']
        df = pd.DataFrame(data, columns=columns)
        
        with self.assertRaises(JoogleChartsException):
            list1 = get_list_from_dataframe(df, allow_nulls=False)
            

    def test_df_to_list_3(self):
        
        # NaN, without allow_nulls
        kids = ['Peter', 'Cindy', "Marsha"]
        pets = [2, 1, np.NaN]
        data = {'kids': kids, 'pets': pets}
        columns = ['kids', 'pets']
        df = pd.DataFrame(data, columns=columns)
        
        with self.assertRaises(JoogleChartsException):
            list1 = get_list_from_dataframe(df, allow_nulls=False)


    def test_df_to_list_4(self):

        # None, with allow_nulls        
        kids = ['Peter', 'Cindy', "Marsha"]
        pets = [2, 1, None]
        data = {'kids': kids, 'pets': pets}
        columns = ['kids', 'pets']
        df = pd.DataFrame(data, columns=columns)
        
        list1 = get_list_from_dataframe(df, allow_nulls=True)

        expected = [['Peter', 2], ['Cindy', 1], ['Marsha', None]]

        self.assertEqual(list1, expected)

    def test_df_to_list_5(self):
        
        # NaN, with allow_nulls
        kids = ['Peter', 'Cindy', "Marsha"]
        pets = [2, 1, np.NaN]
        data = {'kids': kids, 'pets': pets}
        columns = ['kids', 'pets']
        df = pd.DataFrame(data, columns=columns)
        
        list1 = get_list_from_dataframe(df, allow_nulls=True)
        expected = [['Peter', 2], ['Cindy', 1], ['Marsha', None]]

        self.assertEqual(list1, expected)
        
    def test_df_to_datatable(self):
        
        kids = ['Peter', 'Cindy']
        pets = [2, 1]
        dates = [pd.to_datetime("2016-01-01"), pd.to_datetime("2013-02-01")]
        data = {'kids': kids, 'pets': pets, 'dates': dates}
        columns = ['kids', 'pets','dates']
        df = pd.DataFrame(data, columns=columns)
        
        obj = _Data(df)
        
        expected = """var data = new google.visualization.DataTable();
data.addColumn("string", "kids", "0");
data.addColumn("number", "pets", "1");
data.addColumn("date", "dates", "2");
data.addRows(2);
data.setCell(0, 0, "Peter");
data.setCell(0, 1, 2);
data.setCell(0, 2, new Date(2016,0,1));
data.setCell(1, 0, "Cindy");
data.setCell(1, 1, 1);
data.setCell(1, 2, new Date(2013,1,1));
"""
        
        self.assertEqual(obj.data_table.ToJSCode("data"), expected)

    def test_list_to_datatable(self):
        
        headers = ['kids', 'pets', 'dates']
        row1 = ['Peter', 2, date(2016, 1, 1)]
        row2 = ['Cindy', 1, date(2013, 2, 1)]
        data = [headers, row1, row2]
        
        obj = _Data(data)
        
        expected = """var data = new google.visualization.DataTable();
data.addColumn("string", "kids", "0");
data.addColumn("number", "pets", "1");
data.addColumn("date", "dates", "2");
data.addRows(2);
data.setCell(0, 0, "Peter");
data.setCell(0, 1, 2);
data.setCell(0, 2, new Date(2016,0,1));
data.setCell(1, 0, "Cindy");
data.setCell(1, 1, 1);
data.setCell(1, 2, new Date(2013,1,1));
"""

    def test_num_cols_and_rows(self):
        
        kids = ['Peter', 'Cindy', "Jan"]
        pets = [2, 1, 4]
#         dates = [pd.to_datetime("2016-01-01"), pd.to_datetime("2013-02-01"), pd.to_datetime("2011-10-27")]
        data = {'kids': kids, 'pets': pets}
        columns = ['kids', 'pets']
        df = pd.DataFrame(data, columns=columns)
        
        obj = _Data(df)
        
        self.assertEqual(obj.num_cols, 2)
        self.assertEqual(obj.num_rows, 3)
        
        
        
        
        
        
    def test_get_column_names_1(self):
        
        # columns names from dataframe
        
        kids = ['Peter', 'Cindy', "Jan"]
        pets = [2, 1, 4]
#         dates = [pd.to_datetime("2016-01-01"), pd.to_datetime("2013-02-01"), pd.to_datetime("2011-10-27")]
        data = {'kids': kids, 'pets': pets}
        columns = ['kids', 'pets']
        df = pd.DataFrame(data, columns=columns)
        
        obj = _Data(df)
        
        expected = ['kids', 'pets']
        
        self.assertEqual(obj.column_names, expected)
        
        pass
        

    def test_get_column_names_2(self):
        
        # columns names from 2d list
        
        kids = ['Peter', 'Cindy', "Jan"]
        pets = [2, 1, 4]
#         dates = [pd.to_datetime("2016-01-01"), pd.to_datetime("2013-02-01"), pd.to_datetime("2011-10-27")]
        data = {'kids': kids, 'pets': pets}
        columns = ['kids', 'pets']
        df = pd.DataFrame(data, columns=columns)
        
        obj = _Data(df)
        
        expected = ['kids', 'pets']
        
        self.assertEqual(obj.column_names, expected)
        
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()