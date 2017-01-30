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
        # unique string.
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
    
    description = []

    for item in data_row:
        try:
            description_type = translation_dict[type(item)]
        except:
            message = "Data values in the first row must be String, int, float, boolean, date, or datetime."
            raise JoogleChartsException(message)
        description.append(description_type)

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
    
    def __init__(self, datetime_cols = None, allow_nulls=False, *args):
        
        self.dataframe = None
        self.list = None
        self.description = None
        self.json = None
        self.datetime_cols = datetime_cols
        self.allow_nulls = allow_nulls
        self.args = args
    
        self.get_type_of_data_input()
        
        self.check_for_nulls
        
        self.get_description()
        



    def get_type_of_data_input(self):
        
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
                
    def check_for_nulls(self):
        
        pass
    
    def get_description(self):
        if self.dataframe:
            self.description = get_description_from_dataframe(self.dataframe, self.datetime_cols)
        elif self.list:
            self.description = get_description_from_list(self.list)
