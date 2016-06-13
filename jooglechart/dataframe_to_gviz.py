'''
Created on Jun 12, 2016

@author: richd
'''
import gviz_api
import pandas as pd
from utils import JoogleChartsException

def dataframe_to_gviz(cities_df, datetime_cols=None, allow_nulls=False):

    """
    This method takes a pandas data frame and returns a gviz_api DataFrame
    object (or "table").  Use the returned table's ToJSon('[data_name]') to get
    a json string to pass to google.visualization.DataTable() constructor.

    Here are the data types accepted in that constructor, and the pandas
    dtypes that map to them.

    json type values                            pandas dtypes
    ----------------                            -------------------
    boolean                                     bool
    number                                      int64, float64
    string                                      object (*** datetime.date is treated as object by pandas)
    date                                        datetime
    datetime                                    datetime (*** only if datetime_cols are specified)
    timeofday                                   NOT CURRENTLY SUPPORTED HERE

    Reference:  https://developers.google.com/chart/interactive/docs/reference#dataparam

    Notes:
    -- The default js format for pandas datetimes is date.
    -- DATES CREATED WITH PYTHONG'S datetime.date ARE TREATED AS STRINGS IN
       PANDAS. DTYPES RETURNS 'object'.

    Args:
        datetime_cols (list of indexes):  Use datetime instead of date
            for the columns listed by index.
        allow_nulls (boolean):  permit None, Nan, and NaT in dataframe and
            convert them to null values in the js DataTable. (gviz_api converts
            None to null.)
            NOTE:  currently, integer columns become floats if it contains NaN.

    Returns:
        gviz DataTable object.

    Raises:
        JoogleChartsException: generic exception class for any special
            exception.  A message is passed with the details.

    Why use the gviz_api for converting a DataFrame?  There are several ways to generate a
    Javascript DataTable.  See documentation of DataTable class and arrayToDataTable()
    at https://developers.google.com/chart/interactive/docs/reference.  Using
    the api makes it easy to create json for generating the javascript DataTable.
    -- Using json in the constructors can be faster than calling addColumn/addRows
       on an empty DataTable instance.
    -- Data types are specified in json.
    -- gviz_api handles dates automaticaally -- don't need to generate string
       for javascript Date() constructor.
    -- The ToJSCode() method is great for debugging.



    """

    if allow_nulls == False and cities_df.isnull().any().any():
        message = "The DataFrame has null values (None, NaN, or NaT);"
        message += " replace these values, or pass allow_nulls = True to get null"
        message += " values in the javascript DataTable."
        raise JoogleChartsException(message)

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
    for ix, (t, col) in enumerate(zip(cities_df.dtypes, cities_df.columns)):
        if datetime_cols and ix in datetime_cols:
            description.append((col, 'datetime'))
        else:
            description.append((col, translation_dict[t.name]))

    # get a 2d-array of the data
    data = []
    for row in cities_df.iterrows():
        if allow_nulls:

            # isnull detects NaN, NaT, and None.  Nones are converted to js nulls
            r = [None if pd.isnull(item) else item for item in row[1]]
            data.append(r)
        else:
            data.append(row[1].tolist())

    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)

    return data_table


