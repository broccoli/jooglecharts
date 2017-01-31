'''
Created on Jan 27, 2017

@author: richd
'''

import gviz_api
import pandas as pd
from utils import JoogleChartsException
from datetime import datetime, date

def get_description_from_dataframe(df, datetime_cols):
    

    # dictionary to translate pandas dtypes to js DataTable types
    translation_dict= {}
    translation_dict['object'] = 'string'
    translation_dict['float64'] = 'number'
    translation_dict['float32'] = 'number'
    translation_dict['int64'] = 'number'
    translation_dict['int32'] = 'number'
    translation_dict['datetime64[ns]'] = 'date'
    translation_dict['bool'] = 'boolean'

    # get the description with the column names and types
    description = []
    for ix, (t, col) in enumerate(zip(df.dtypes, df.columns)):
        if datetime_cols and ix in datetime_cols:
            t = 'datetime'
        else:
            t = translation_dict[t.name]

        # gviz_api takes various formats for table description.  We're using
        # the ('id', 'type', 'label') format.  The id just needs to be an arbitrary
        # unique string.  We'll use a string of the index.
        description.append((str(ix), t, col))
        
    return description

def get_description_from_list(list1):
    
    # a list has to contain at least one header row and one data row
    if len(list1) < 2:
        message = "A 2d list of data must have one header row and at least one data row"
        raise JoogleChartsException(message)
        
    # loop through the first data row and get the datatypes
    data_row = list1[1]
    
    translation_dict= {}
    translation_dict[str] = 'string'
    translation_dict[int] = 'number'
    translation_dict[float] = 'number'
    translation_dict[bool] = 'boolean'
    translation_dict[date] = 'date'
    translation_dict[datetime] = 'datetime'
    
    types = []

    for item in data_row:
        try:
            description_type = translation_dict[type(item)]
        except:
            message = "Data values in the first row must be String, int, float, boolean, date, or datetime."
            raise JoogleChartsException(message)
        types.append(description_type)

    headers = list1[0]
    description = []
    for ix, (t, col) in enumerate(zip(types, headers)):
        description.append((str(ix), t, col))
        
    return description


def get_list_from_dataframe(df, allow_nulls):
    
    # get a 2d-array of the data
    data = []
    for row in df.iterrows():
        if allow_nulls:

            # isnull detects NaN, NaT, and None.  Nones are converted to js nulls
            r = [None if pd.isnull(item) else item for item in row[1]]
            data.append(r)
        else:
            data.append(row[1].tolist())
            
    return data


class _Data():
    
    """
    The Data class handles various data functions for the jooglechart.
    
    Data can be provided in several different formats:  a pandas dataframe,
    a series of pandas Series, or a 2d list (a list or rows).
    If the data is provided in a list, the first row is the headers.
    
    Data must be fed in the javascript to the google.visualization.DataTable() constructor.
    The constructor can create a data table in several different ways, including from json.
    We are using json.  The json can be generated using gviz_api.  The gviz_api creates a table
    using a description of the data, and then data itself in a 2d list.  Json can then be
    generated from the gviz table.
    
    Using gviz table and json has several advantages.
    -- Using json in the constructors can be faster than calling addColumn/addRows
       on an empty DataTable instance.
    -- Data types are specified in json.
    -- gviz_api handles dates automatically -- don't need to generate a string
       for javascript Date() constructor.
    -- The gviz method ToJSCode() method is great for debugging and testing.

    Data types in DataTable
    The Google DataTable accepts several data types, which can be found here:
    https://developers.google.com/chart/interactive/docs/reference#dataparam
    
    The type timeofday is not currently supported in jooglechart.


    """
    
    def __init__(self, datetime_cols = None, allow_nulls=False, *args):
        
        self.dataframe = None
        self.list = None
        self.description = None
        self.json = None
        self.datetime_cols = datetime_cols
        self.allow_nulls = allow_nulls
        self.args = args
        
        # for now, just using the data_table for unit testing
        self.data_table = None
    
        self.get_type_of_data_input()
        
        # if we have a dataframe, turn it into a 2d list
        if self.dataframe:
            self.list = get_list_from_dataframe()
        
        self.check_df_for_nulls()
        
        self.create_gviz_description()
        
        # generate json for the Google DataTable
        self.data_table = gviz_api.DataTable(self.description)
        self.data_table.LoadData(self.list)
        
        self.json = self.data_table.ToJSon()


    def get_type_of_data_input(self):
        
        """
        See what kind of format the data is in, and store data as a dataframe or list
        """
        
        args = self.args
        if len(args) == 1:
            # check if data is a dataframe or 2d list

            data = args[0]
            if isinstance(data, pd.DataFrame):
                self.dataframe = data
            elif (isinstance(data, list) and isinstance(data[0], list)):
                self.list = data
            else:
                message = "Data must be passed as 2d list, a DataFrame, or 2 or more Series"
                raise JoogleChartsException(message)
        else:
            # Data can only be Series at this point
            try:
                # make dataframe out of series
                df = pd.DataFrame(args[0])
                for s in args[1:]:
                    df[s.name] = s

            except:
                message = "Data must be passed as 2d array, a DataFrame, or 2 or more Series"
                raise JoogleChartsException(message)
            self.dataframe = df
                
    def check_df_for_nulls(self):
        
        if self.dataframe and self.allow_nulls == False and self.dataframe.isnull().any().any():
            message = "The DataFrame has null values (None, NaN, or NaT);"
            message += " replace these values, or pass allow_nulls = True to get null"
            message += " values in the javascript DataTable."
            raise JoogleChartsException(message)
    
    def create_gviz_description(self):
        if self.dataframe:
            self.description = get_description_from_dataframe(self.dataframe, self.datetime_cols)
        elif self.list:
            self.description = get_description_from_list(self.list)
