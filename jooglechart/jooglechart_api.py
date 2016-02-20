# -*- coding: utf-8 -*-

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

'''
Running todo list
-- add roles / tooltips (not sure how to handle all of it)
-- add google sheet data load
-- position filter on top or bottom?
-- add style palettes (colors, font)?
-- add title banner, like Tableau?
-- all text in chart row column?


'''

import copy
import os
import gviz_api
import pandas as pd
import json
from IPython.display import display, HTML



from jinja2 import Environment, FileSystemLoader

from jinja_filters import to_json, format_styles_list





DEFAULT_CHART_TYPE = "ColumnChart"

# ISHBOOK-495
BASE_NOTEBOOK_URL = "https://ishbook.corp.indeed.com/nb/{nbid}/dashboard/{qs}"

# Set up Jinja
PATH = os.path.dirname(os.path.abspath(__file__))
loader=FileSystemLoader(os.path.join(PATH, 'jinja_templates'))
j2_env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
j2_env.filters['to_json'] = to_json
j2_env.filters['format_styles_list'] = format_styles_list


class PythonGoogleChartsException(Exception):
    """ General exception object thrown by python google charts API """
    pass


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

    if allow_nulls == False and cities_df.isnull().any().any():
        message = "The DataFrame has null values (None, NaN, or NaT);"
        message += " replace these values, or pass allow_nulls = True to get null"
        message += " values in the javascript DataTable."
        raise PythonGoogleChartsException(message)

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



### Keep a running counter for all instances of JugChart.
### The counter is appended to the div's id to insure that each id is unique
chart_counter = [0]
formatter_counter = [0]
filter_counter = [0]
juggle_chart_counter = [0]

def get_counter(counter_list):
    counter_list[0] += 1
    return counter_list[0]

def get_chart_counter():
    return get_counter(chart_counter)
def get_formatter_counter():
    return get_counter(formatter_counter)
def get_filter_counter():
    return get_counter(filter_counter)
def get_jugle_chart_counter():
    return get_counter(juggle_chart_counter)



class Filter(object):

    """
    filter object that you pass to a chart object.
    By default binds the data.  But can bind another filter.
    """

    def __init__(self, type):
        self.type = type
        self.options = {}
        self.state = {}
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

        if self.options == None:
            self.options = {}
        if options:
            _add_dict_to_dict(self.options, options)

        if kwargs:
            _add_dict_to_dict(self.options, kwargs)



    def add_state(self, state = None, **kwargs):

        if self.state == None:
            self.state = {}
        if state:
            _add_dict_to_dict(self.state, state)

        if kwargs:
            _add_dict_to_dict(self.state, kwargs)

    def bind_filter(self, bind_target):
        self.bind_target = bind_target
        
        if isinstance(bind_target, SeriesFilter):
            message = "Cannot bind a SeriesFilter"
            raise PythonGoogleChartsException(message)

    def _set_render_properties(self):
        self.num = get_filter_counter()
        self.name = "google_filter_" + str(self.num)
        self.div_id = self.name + "_div_id"


class SeriesFilter(Filter):
    
    """
    A SeriesFilter filters columns of data that are represented as series
    of columns, lines, etc.
    
    A SeriesFilter can apply to JoogleCharts with multiple charts, but each
    one must have the same columns used as series.  That is, they must have the 
    same visible columns.
    
    When determining the series columns, role columns will be skipped, and the 
    first visible non-role columns (since it is the category, or y-axis).
    """
    
    def __init__(self):
        super(SeriesFilter, self).__init__(None)
#         Filter.__init__(self, None)
        self.add_options(ui_label = "Columns")
        self.add_options(filterColumnIndex = 0)

    def add_options(self, options = None, **kwargs):
        
        message = "filter column is automatically set on a SeriesFilter"
        if options and (("columnFilterIndex" in options) or ("columnFilterLabel" in options)):
            raise PythonGoogleChartsException(message)
        if kwargs.get("columnFilterIndex") or kwargs.get("columnFilterLabel"):
            raise PythonGoogleChartsException(message)

        super(SeriesFilter, self).add_options(options, **kwargs) 

    def bind_filter(self, *args):
        
        message = "data is automatically bound on a SeriesFilter"
        raise PythonGoogleChartsException(message)

    def _set_render_properties(self, jooglechart):
        
        # check if all charts have the same view cols
        if len(jooglechart.charts) > 1:
            charts = jooglechart.charts
            view_cols = charts[0]
            for chart in charts[1:]:
                if chart.view_cols != view_cols:
                    message = "For SeriesFilter, all charts must have the same view cols"
                    raise PythonGoogleChartsException(message)
        
        # get a list of series columns
        try:
            columns = jooglechart._dataframe.columns.values.tolist()
        except:
            # TODO: data is in a 2d array
            columns = jooglechart._2d_array[0]
        # null out the role columns
        role_cols = [role[0] for role in jooglechart.roles]
        columns = []
        
        print columns
        
        
        self.num = get_filter_counter()
        self.name = "series_filter_" + str(self.num)
        self.div_id = self.name + "_div_id"

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



def _add_dict_to_dict(current_options, options_dict):

    # before combining the dictionaries, convert keywords that are
    # in underscore or dot notation into nested dictionaries
#     new_dict = {}
    new_dicts = []
    for k, v in options_dict.iteritems():
        k2 = k.replace('_', '.')
        if '.' in k2:
            nested_dict = _get_nested_dict_from_dotted_key(k2, v)


            new_dicts.append(nested_dict)

        else:
            new_dicts.append({k: v})


    for d in new_dicts:
        _add_nested_dict_to_dict(current_options, d)

def _get_nested_dict_from_dotted_key(key, val):
    # A dotted k_v_tuple is like this:  ("style.font.color", "#FF0000")
    # converts to this: {"style": {"font": {"color": "#FF0000"}}}

    key_list = key.split(".")
    return_dict = {}
    for key in key_list[1:][::-1]:
        new_dict = {key:val}
        val = new_dict
    return_dict[key_list[0]] = val

    return return_dict

def _add_nested_dict_to_dict(current_dict, input_dict):

    """
    This method adds one dictionary to another.  It's similar to
    dictionary .update(), but it will loop through levels of nested
    dictionaries and update at the lowest possible level.

    (Currently, the input dictionary can only have one item in any dictionary.
    To handle multiple items, need to use recursion.)

    Example 1, non-nested dictionaries, behaves like .update():
    d1 = {'a': 5}
    d2 = {'b': 6}
    _add_nested_dict_to_dict(d1, d2)
    print d1 # {'a': 5, 'b': 6}

    Example 2, with nested dictionaries:
    d1 = {'a': {'b': 3} }
    d2 = {'a': {'c': 4} }
    _add_nested_dict_to_dict(d1, d2)
    print d1 # {'a': {'b': 3, 'c': 4}}

    """

    right_dict = input_dict
    left_dict = current_dict

    for k, v in right_dict.iteritems():

        if not k in left_dict:
            # if the k is not in the dict, it's new, so add it.
            left_dict[k] = v
            continue
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
                continue
            else:

                # Here, the dictionary on the left continues the same chain
                # as the left, so advance to the next value to look for a
                # new dict value.
                right_dict = v
                left_dict = left_dict[k]
                _add_nested_dict_to_dict(left_dict, right_dict)


class _Chart():

    def __init__(self, chart_type=None, **kwargs):

        # Chart attributes
        if chart_type == None:
            chart_type = DEFAULT_CHART_TYPE
        self.chart_type = chart_type
        self.display_chart_type = None
        self.chart_options = {}
        self.div_styles = {}
#         self.hide_cols = None
        self.view_cols = None
#         self.display_cols = None
        self.chart_div_id = None
        self.num = None
        self.name = None

        # add any leftover kwargs to options
        if kwargs:
            self.add_chart_options(**kwargs)

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

        if options == None and not kwargs:
            # user is resetting options

            self.chart_options = {}
        else:
            if options == None:
                options = {}
            if kwargs:
                options.update(kwargs)

            _add_dict_to_dict(self.chart_options, options)


    def add_div_styles(self, style_dict = None, **kwargs):
        """
        pass styles for the chart div in a dictionary or as keyword arguments
        """

        if self.div_styles == None:
            self.div_styles = {}

        if style_dict == None and not kwargs:
            # user is resetting styles

            self.div_styles = {}
        else:
            if style_dict == None:
                style_dict = {}
            if kwargs:
                style_dict.update(kwargs)
            _add_dict_to_dict(self.div_styles, style_dict)


    def set_view_cols(self, cols):

        if isinstance(cols, int):
            cols = [cols]
        self.view_cols = cols


    def _set_render_properties(self, num_cols, chart_type=None):

        # chart render properties
        self.num = get_chart_counter()
        self.name = "google_chart_" + str(self.num)
        self.chart_div_id = self.name + "_div_id"

        # set chart options to empty dict if it's been nulled out
        if self.chart_options == None:
            self.chart_options = {}



        # set chart type to display
        if chart_type == None:
            self.display_chart_type = self.chart_type
        else:
            self.display_chart_type = chart_type

class Styler():
    
    def apply_styles(self, chart):
        raise NotImplementedError('subclasses must override apply_styles()!')
        

class JoogleChart():

    def __init__(self, *args, **kwargs):

        # jg attributes
        self.num = None
        self.name = None
        self.charts = []

        # Data attributes
        self._2d_array = None
        self.formatters = []
        self.filters = []
        self.datetime_cols = kwargs.pop('datetime_cols', None)
        self.allow_nulls = kwargs.pop('allow_nulls', False)
        self.json = None
        self.roles = []
        self.tooltip_html = False
        self._series_filter = None
        self._dataframe = None

        # Dashboard attributes
        self.load_controls = False
        self.dashboard_div_id = None

        # Chart attributes
        chart_type = kwargs.pop('chart_type', DEFAULT_CHART_TYPE)

        self.charts.append(_Chart(chart_type))

        # add any leftover kwargs to options
        if kwargs:
            self.charts[0].add_chart_options(**kwargs)

        # data can be passed as a 2d array, a DataFrame or 2 or more Series
        if len(args) == 1:
            # check if data is a dataframe or 2d list

            data = args[0]
            if isinstance(data, pd.DataFrame):
                table = dataframe_to_gviz(data, datetime_cols=self.datetime_cols, allow_nulls=self.allow_nulls)
                self.json = table.ToJSon()
                self._dataframe = data
            elif (isinstance(data, list) and isinstance(data, list)):
                self._2d_array = data
        else:
            # Data can only be Series at this point
            try:

                cities_df = pd.DataFrame(args[0])
                for s in args[1:]:
                    cities_df[s.name] = s

            except:
                message = "Data must be passed as 2d array, a DataFrame, or 2 or more Series"
                raise PythonGoogleChartsException(message)
            self._dataframe = cities_df
            table = dataframe_to_gviz(cities_df, datetime_cols=self.datetime_cols, allow_nulls=self.allow_nulls)
            self.json = table.ToJSon()


    def add_chart_options(self, options=None, **kwargs):

        self.charts[0].add_chart_options(options, **kwargs)

    def set_view_cols(self, *args, **kwargs):
        self.charts[0].set_view_cols(*args, **kwargs)


    def set_chart_type(self, chart_type):

        self.charts[0].chart_type = chart_type

    def add_formatter(self, formatter, options=None, cols=None, source_cols=None, pattern=None, dest_col=None):

        """
        Formatters all require chart_options and col, except for PatternFormat.  PatternFormat
        requires pattern, source_cols, and col.
        """

        if self.formatters == None:
            self.formatters = []

        self.formatters.append(Formatter(formatter, options=options, cols=cols,
                source_cols=source_cols, pattern=pattern, dest_col=dest_col))


    def add_filter(self, filter):
        
        if isinstance(filter, SeriesFilter):
            self._add_series_filter(filter)
            return
        if self.filters == None:
            self.filters = []
        self.filters.append(filter)
        self.load_controls = True

    def _add_series_filter(self, filter):
        
        self._series_filter = filter

    def set_role(self, col, role):

        if self.roles == None:
            self.roles = []
        if not col and not role:
            message = "col and role are required parameters."
            raise PythonGoogleChartsException(message)

        self.roles.append((col, role))

    def set_tooltip(self, col, html=False):
        self.set_role(col, 'tooltip')
        self.tooltip_html = html

    def add_div_styles(self, *args, **kwargs):

        self.charts[0].add_div_styles(*args, **kwargs)

    def _add_chart(self, chart):
        self.charts.append(chart)

    def copy(self):

        return copy.deepcopy(self)

    def _set_render_properties(self, chart_type=None):

        """
        Set values needed for rendering the chart
        """


        # jg render properties
        self.num = get_jugle_chart_counter()
        self.name = "jugle_chart_" + str(self.num)
        self.data_name = self.name + "_data"
        self.view_name = self.name + "_view"
        self.dashboard_name = self.name + "_dashboard"
        self.dashboard_div_id = self.dashboard_name + "_div_id"


        if self.json:
            # data is in a dataframe
            num_cols = len(self._dataframe.columns)

            # unicode            
            # Need to wrap the decoding in a try block so the user will be able to reshow
            # a chart in Jupyter.  If you reshow a chart, the code below will 
            # try to decode an already decoded string.         
            try:
                self.json = self.json.decode('utf-8')
            except UnicodeEncodeError:
                pass
        else:
            # data is in a 2d array
            num_cols = len(self.data[0])

        # set the visible columns if hide_cols is set
        # get the number of columns
        for index, chart in enumerate(self.charts):
            if index == 0:
                chart._set_render_properties(num_cols, chart_type)
            else:
                chart._set_render_properties(num_cols)

        for filter_ in self.filters:
            filter_._set_render_properties()

        if self._series_filter:
            self._series_filter._set_render_properties(self)

        # modify json with roles
        if self.roles:
            json_decode = json.loads(self.json)
            for col, role in self.roles:
                if role == 'tooltip' and self.tooltip_html:
                    json_decode['cols'][col].update({'p': {'role': role, 'html': True}})
                    self.add_chart_options(tooltip_isHtml = True)
                else:
                    json_decode['cols'][col].update({'p': {'role': role}})
            self.json = json.dumps(json_decode)


    def render(self, chart_type=None):

        """
        Render chart code.
        chart_type is one-off type; not saved to underlying chart.
        """
        self._set_render_properties(chart_type)

        context = {}
        context['jg'] = self
        context['load_controls'] = self.load_controls
        context['callback_name'] = 'doStuff_' + str(self.num)
        context['google_loader_name'] = 'google_loader_' + str(self.num)

        # ISHBOOK-495
        context['notebook_url'] = _get_notebook_url()


        return j2_env.get_template('chart_template.html').render(context).encode('utf-8')


    def show(self, chart_type=None, **kwargs):

        """
        .show creates chart with one-off chart type and style options.
        They aren't saved to the underlying chart.
        """

        # any leftover kwargs are assumed to be chart options
        chart = self.copy()
        if kwargs:
            chart.add_chart_options(**kwargs)
        else:
            chart = self
        display(HTML(chart.render(chart_type)))


class ChartRow:

    """
    A ChartRow can create a row of charts to display side-by-side.  Currently,
    The charts are rendered in 2-4 bootstrap columns of equal size.

    Pass 2-4 chart objects to the constructor.
    """

    def __init__(self, *jcs):

        self.jcs = jcs
        self.num_jcs = len(self.jcs)
        self.load_controls = False

        if self.num_jcs not in [2, 3, 4]:
            message = "A chart row must have 2-4 charts"
            raise PythonGoogleChartsException(message)

        self.bootstrap_num = 12 / self.num_jcs



    def render(self):

        self.num = get_jugle_chart_counter()

        for jc in self.jcs:
            if jc.filters:
                self.load_controls = True
                break

        for jc in self.jcs:
            jc._set_render_properties()

        context = {}
        context['chartrow'] = self
        context['load_controls'] = self.load_controls
        context['callback_name'] = 'doStuff_' + str(self.num)
        context['google_loader_name'] = 'google_loader_' + str(self.num)

        # ISHBOOK-495
        context['notebook_url'] = _get_notebook_url()

        return j2_env.get_template('chartrow_template.html').render(context).encode('utf-8')

    def show(self):

        display(HTML(self.render()))

# ISHBOOK-495
def _is_real_ishbook(frame_globals):
    try:
        return "__nbparams__" in frame_globals
    except (KeyError, AttributeError):
        return False

# ISHBOOK-495
def _frame_globals():
    import inspect
    frame_globals = {}
    for frame in inspect.stack():
        if '__nbparams__' in frame[0].f_globals:
            return frame[0].f_globals
    return {}

# ISHBOOK-495
# Hack to get the notebook id if in the ishbook context.
def _get_nbid(frame_globals):
    ls_dict = frame_globals["__nbparams__"]["__meta__"]["lookup_service"]
    return json.loads(ls_dict["data"])["notebook"]

# ISHBOOK-495
# Hack to get the notebook params if in the ishbook context.
def _get_nbparams(frame_globals):
    params = frame_globals["__nbparams__"]
    return {k: v for (k, v) in params.iteritems() if k != "__meta__"}

# ISHBOOK-495
def _get_notebook_url():
    import urllib
    fg = _frame_globals()
    if _is_real_ishbook(fg):
        (nbid, nbparams) = (_get_nbid(fg), _get_nbparams(fg))
        qs = urllib.urlencode(nbparams, doseq=True)
        return BASE_NOTEBOOK_URL.format(nbid=nbid, qs=qs)
    else:
        return ''

def _gplot(self, chart_type=None, **kwargs):

    chart = JoogleChart(self)
    if kwargs:
        chart.add_chart_options(kwargs)
    chart.show(chart_type)

pd.DataFrame.gplot = _gplot
