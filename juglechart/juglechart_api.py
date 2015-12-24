'''
Created on Dec 5, 2015

@author: richd


DEPENDENCIES:

    Python
    ------
    * gviz_api -- pip install from https://github.com/google/google-visualization-python
        gviz_api allows creation of javascript DataTable in python.
    * pandas
    * ipython
    * jinja2
    
    Javascript
    ----------
    * jQuery


    TODO:
       
    Demo notebooks to make
    -- basic demo
        -- acceptable dataformats
        -- allow_nulls
        -- passing chart_options for chart
        -- passing styles for container
    -- formatters demo
    -- common options
    -- chart types demo
    -- filters demo
    -- chart row

'''

import copy
import json
import os
import gviz_api
import pandas as pd
from IPython.display import display, HTML 

from jinja2 import Environment, FileSystemLoader




DEFAULT_CHART_TYPE = "ColumnChart"


PATH = os.path.dirname(os.path.abspath(__file__))
loader=FileSystemLoader(os.path.join(PATH, 'jinja_templates'))
j2_env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

def to_json(s):
    return json.dumps(s)

def format_styles_list(div_styles):

    if div_styles:
        style_base = "%s: %s"
        style_list = []
        for k, v in div_styles.iteritems():
            style_list.append(style_base % (k, v))
        return 'style="%s"' % "; ".join(style_list)
    else:
        return ""

j2_env.filters['to_json'] = to_json
j2_env.filters['format_styles_list'] = format_styles_list


class PythonGoogleChartsException(Exception):
    """ General exception object thrown by python google charts API """
    pass


def dataframe_to_gviz(df, datetime_cols=None, allow_nulls=False):

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
        PythonGoogleChartsException: generic exception class for any special
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
    
    if allow_nulls == False and df.isnull().any().any():
        message = "The DataFrame has null values (None, NaN, or NaT);"
        message += " replace these values, or pass allow_nulls = True to get null"
        message += " values in the javascript DataTable."
        raise PythonGoogleChartsException(message)

    # dictionary to translate pandas dtypes to js DataTable types
    translation_dict= {}
    translation_dict['object'] = 'string'
    translation_dict['float64'] = 'number'
    translation_dict['int64'] = 'number'
    translation_dict['datetime64[ns]'] = 'date'
    translation_dict['bool'] = 'boolean'
    
    # get the description with the column names and types
    description = []
    for ix, (t, col) in enumerate(zip(df.dtypes, df.columns)):
        if datetime_cols and ix in datetime_cols:
            description.append((col, 'datetime'))
        else:
            description.append((col, translation_dict[t.name]))

    # get a 2d-array of the data
    data = []
    for row in df.iterrows():
        if allow_nulls:
            
            # isnull detects NaN, NaT, and None.  Nones are converted to js nulls
            r = [None if pd.isnull(item) else item for item in row[1]]
            data.append(r)
        else:
            data.append(row[1].tolist())

    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)

    return data_table
        


### Keep a running counter for all instances of JugChart.
### The counter is appended to the div's id to insure that each id is unique
div_id_counter = [0]
formatter_counter = [0]
filter_counter = [0]

def get_counter(counter_list):
    counter_list[0] += 1
    return counter_list[0]

def get_div_id_counter():
    return get_counter(div_id_counter)
def get_formatter_counter():
    return get_counter(formatter_counter)
def get_filter_counter():
    return get_counter(filter_counter)



class Filter():
    
    """
    filter object that you pass to a chart object.
    By default binds the data.  But can bind another filter.
    """
    
    def __init__(self, type):
        self.type = type
        self.options = {}
        self.state = {}
    
        self.num = get_filter_counter()
        self.name = "google_filter_" + str(self.num)
        self.div_id = self.name + "_div_id"
        self.bind_target = None


    def add_options(self, options = None, **kwargs):
        """
        pass chart chart_options in a dictionary and/or as keyword arguments
        
        options that are nested javascript object properties can be indicated with 
        dots. or underscores.  For example, hAxis.direction be passed in these ways
        
        add_chart_options(hAxis_direction = 1)
        add_chart_options({'hAxis_direction': 1)
        add_chart_options({'hAxis.direction': 1)
        
        The full json notation can also be used:
        
        add_chart_options({'hAxis': {'direction': 1}})
        
        """
        
        if options:
            add_options_dict_to_dict(self.options, options)
    
        if kwargs:
            add_options_dict_to_dict(self.options, kwargs)

        
    
    def add_state(self):
        
        # TODO
        pass

    def bind_filter(self, bind_target):
        self.bind_target = bind_target



class Formatter():
    
    FORMATTER_TYPES = ['ArrowFormat', 'BarFormat', 'ColorFormat', 'DateFormat', 'NumberFormat', 'PatternFormat']
    FORMATTER_TYPES_LOWER = ['arrow', 'bar', 'color', 'date', 'number', 'pattern']

    
    def __init__(self, type=None, options=None, cols=None, source_cols=None, dest_col=None, pattern=None):


        # validate formatter type
        try:
            formatter_ix = self.FORMATTER_TYPES.index(type)
        except ValueError:
            try:
                formatter = type.lower()
                formatter_ix = self.FORMATTER_TYPES_LOWER.index(formatter)
            except ValueError:
                message = "Format type submitted is not valid"
                raise PythonGoogleChartsException(message)
            
        type = self.FORMATTER_TYPES[formatter_ix]

        if type == "ColorFormat":
            message = "ColorFormat is not currently supported"
            raise PythonGoogleChartsException(message)
        

        if type == 'PatternFormat':
            if source_cols is None or pattern is None:
                message = "PatternFormat requires source_cols and pattern"
                raise PythonGoogleChartsException(message)
        elif cols is None or options is None:
            message = "This format requires options and cols"
            raise PythonGoogleChartsException(message)
        

        self.type = type
        self.options = options
        if isinstance(cols, int):
            cols = [cols]
        self.cols = cols
        self.source_cols = source_cols
        if self.type == "PatternFormat" and dest_col == None:
            self.dest_col = self.source_cols[0]
        else:
            self.dest_col = dest_col
        self.pattern = pattern
        
        self.num = get_formatter_counter()
        self.name = "formatter" + str(self.num)
        
        
        
def add_options_dict_to_dict(current_options, options_dict):
    for k, v in options_dict.iteritems():
        k2 = k.replace('_', '.')
#         key_list = k2.split(".")

        nested_dict = create_nested_dict_from_dotted_key((k2, v))
        add_nested_dict_to_dict(current_options, nested_dict)


def create_nested_dict_from_dotted_key(k_v_tuple):
    # A dotted k_v_tuple is like this:  ("style.font.color", "#FF0000")
    # converts to this: {"style": {"font": {"color": "#FF0000"}}}
    
    key, val = k_v_tuple
    key_list = key.split(".")
    return_dict = {}
    for key in key_list[1:][::-1]:
        new_dict = {key:val}
        val = new_dict
    return_dict[key_list[0]] = val
    
    return return_dict
    
        
def add_nested_dict_to_dict(current_dict, input_dict):
    
    right_dict = input_dict
    left_dict = current_dict
    go_on = True
    
    while go_on:
        
        for k, v in right_dict.iteritems():
            
            if not k in left_dict:
                # if the k is not in the dict, it's new, so add it.
                left_dict[k] = v
                go_on = False
                break
            else:

                # Now we know that the right key is in the left
                if (not isinstance(left_dict[k], dict)) or (not isinstance(right_dict[k], dict)):
                    # In some cases we are going to overwrite the left value
                    # with the right.  We are assuming that the developer wants to
                    # overwrite a value that has been previously set.
                    # These case are:
                    #    1. The left value is not a dictionary
                    #    2. Or, the right value is not a dictionary
                    # In either case, the chain of dictionaries has ended.
                    left_dict[k] = right_dict[k]
                    go_on = False
                    break
                else:
                    right_keys = v.keys()
                    left_keys = left_dict[k].keys()
                    if not set(right_keys).issubset(set(left_keys)):
                        left_dict[k].update(v)
                        go_on = False
                        break
                    
                    # Here, the dictionary on the left continues the same chain
                    # as the left, so advance to the next value to look for a
                    # new dict value.
                    right_dict = v
                    left_dict = left_dict[k]
                                
    

class JugleChart():
    
    def __init__(self, *args, **kwargs):
        
        self.chart_type = kwargs.pop('chart_type', DEFAULT_CHART_TYPE)
        self.display_chart_type = None
        self.chart_options = {}
        self.data = None
        self.formatters = []
        self.div_styles = {}
        self.filters = []
        self.load_controls = False
        self.datetime_cols = kwargs.pop('datetime_cols', None)
        self.hide_cols = None
        self.display_cols = None
        self.json = None

        self.chart_div_id = None
        self.dashboard_div_id = None
        self.num = None

        # data can be passed as a 2d array, a DataFrame or 2 or more Series
        if len(args) == 1:
            # check if data is a dataframe or 2d list
            
            data = args[0]
            if isinstance(data, pd.DataFrame):
                table = dataframe_to_gviz(data, datetime_cols=self.datetime_cols)
                self.json = table.ToJSon()
                self.data_frame = table
            elif (isinstance(data, list) and isinstance(data, list)):
                self.data = data
        else:
            # Data can only be Series at this point
            try:
                
                df = pd.DataFrame(args[0])
                for s in args[1:]:
                    df[s.name] = s
                
            except:
                message = "Data must be passed as 2d array, a DataFrame, or 2 or more Series"
                raise PythonGoogleChartsException(message)
            self.data_frame = df
            table = dataframe_to_gviz(df)
            self.json = table.ToJSon()
        
        
        
    def add_chart_options(self, options = None, **kwargs):
        """
        pass chart chart_options in a dictionary and/or as keyword arguments
        
        options that are nested javascript object properties can be indicated with 
        dots. or underscores.  For example, hAxis.direction be passed in these ways
        
        add_chart_options(hAxis_direction = 1)
        add_chart_options({'hAxis_direction': 1)
        add_chart_options({'hAxis.direction': 1)
        
        The full json notation can also be used:
        
        add_chart_options({'hAxis': {'direction': 1}})
        
        """
        
        # Set chart to empty dictionary if user has nulled it out.
        if self.chart_options == None:
            self.chart_options = {}
        
        if options:
            add_options_dict_to_dict(self.chart_options, options)
    
        if kwargs:
            add_options_dict_to_dict(self.chart_options, kwargs)
        
    
    def add_div_styles(self, style_dict = None, **kwargs):
        """
        pass styles for the chart div in a dictionary or as keyword arguments
        """
        if style_dict:
            add_options_dict_to_dict(self.div_styles, style_dict)
    
        if kwargs:
            add_options_dict_to_dict(self.div_styles, kwargs)

    
    def add_formatter(self, formatter, options=None, cols=None, source_cols=None, pattern=None, dest_col=None):
        
        """
        Formatters all require chart_options and col, except for PatternFormat.  PatternFormat
        requires pattern, source_cols, and col.
        """
        
        self.formatters.append(Formatter(formatter, options=options, cols=cols,
                source_cols=source_cols, pattern=pattern, dest_col=dest_col))

    
    def add_filter(self, filter):
        
        self.filters.append(filter)
        self.load_controls = True
        
    def set_role(self, col, role):
        
        #TODO
        pass
    
    
    def copy(self):
        
        return copy.deepcopy(self)
    
    def set_render_properties(self, chart_type=None):
        
        # set the chart div id on rendering, so the chart can be displayed
        # multiple times with unique ids.
        self.num = get_div_id_counter()
        self.name = "google_chart_" + str(self.num)
        self.data_name = self.name + "_data"
        self.view_name = self.name + "_view"
        self.chart_div_id = self.name + "_div_id"
        self.dashboard_name = self.name + "_dashboard"
        self.dashboard_div_id = self.dashboard_name + "_div_id"

        # set chart options to empty dict if it's been nulled out
        if self.chart_options == None:
            self.chart_options = {}
        
        # set the visible columns if hide_cols is set
        # get the number of columns
        if self.hide_cols:
            
            if isinstance(self.hide_cols, int):
                self.hide_cols = [self.hide_cols]
            
            if self.json:
                # data is in a dataframe
                num_cols = len(self.data_frame.columns)
            else:
                # data is in a 2d array
                num_cols = len(self.data[0])
            self.display_cols = [ix for ix in range(num_cols) if ix not in self.hide_cols]
        
        if chart_type == None:
            self.display_chart_type = self.chart_type
        else:
            self.display_chart_type = chart_type
    
    def render(self, chart_type=None):
        
        self.set_render_properties(chart_type)

        return j2_env.get_template('chart_template.html').render(chart=self, load_controls=self.load_controls)

        
    def show(self, chart_type=None):
        
        return display(HTML(self.render(chart_type)))


class ChartRow:
    
    """
    A ChartRow can create a row of charts to display side-by-side.  Currently,
    The charts are rendered in 2-4 bootstrap columns of equal size.
    
    Pass 2-4 chart objects to the constructor.
    """
    
    def __init__(self, *charts):
        
        self.charts = charts
        self.num_charts = len(self.charts)
        self.load_controls = False
        
        if self.num_charts not in [2, 3, 4]:
            message = "A chart row must have 2-4 charts"
            raise PythonGoogleChartsException(message)
        
        self.bootstrap_num = 12 / self.num_charts
        for chart in self.charts:
            if chart.filters:
                self.load_controls = True
                break
                

    def render(self):
        
        for chart in self.charts:
            chart.set_render_properties()
            
        return j2_env.get_template('chartrow_template.html').render(chartrow=self, load_controls=self.load_controls)
        
    def show(self):

        return display(HTML(self.render()))
