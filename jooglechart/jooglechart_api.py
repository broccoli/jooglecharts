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
import pandas as pd
import json
from IPython.display import display, HTML

from utils import get_joogle_object_counter, set_common_on_context, j2_env, JoogleChartsException, _add_dict_to_dict
from dataframe_to_gviz import dataframe_to_gviz

import sonar_keys


DEFAULT_CHART_TYPE = "ColumnChart"
FILTER_NAME_ADD_ON = "__jooglechart_user_filter_name"  # deprecated, for super filter

class _GoogleFilter(object):
    
    def __init__(self, type):
        self._type = type
        self._options = {}
        self._state = {}
        self._bind_target = None
        self._name = None
        self._global_name = False
        self._senders = []
        self._receivers = []

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

        if self._options == None:
            self._options = {}
        if options:
            _add_dict_to_dict(self._options, options)

        if kwargs:
            _add_dict_to_dict(self._options, kwargs)

    def add_state(self, state = None, **kwargs):

        if self._state == None:
            self._state = {}
        if state:
            _add_dict_to_dict(self._state, state)

        if kwargs:
            _add_dict_to_dict(self._state, kwargs)

    def add_sender(self, key, on="statechange", type='send_selection'):
        # possible types:
        #   send date range
        #   send number range
        
        self._senders.append({'on': on, 'key': key, 'type': type})
                
    
    def add_receiver(self, key, action="update_selection"):
        
        # possible actions
        #  update date range
        #  update number range
        
        self._receivers.append({'key': key, 'action': action})


    def _set_render_properties(self):
        raise JoogleChartsException("_set_render_properties not implemented")
        


class Filter(_GoogleFilter):

    """
    filter object that you pass to a chart object.
    By default binds the data.  But can bind another filter.
    """

    def __init__(self, type):
        super(Filter, self).__init__(type)
        self._label = None
        self._json = None
        self._data_type = None

    def bind_filter(self, bind_target):
        self._bind_target = bind_target
        
        if isinstance(bind_target, SeriesFilter):
            message = "Cannot bind a SeriesFilter"
            raise JoogleChartsException(message)

    def set_filter_label(self, label):
        
        # deprecated function for super category filter target
        
        self._label = label

    def add_values_series(self, series):
        df = pd.DataFrame(series)
        table = dataframe_to_gviz(df, allow_nulls=True)
        self._json = table.ToJSon()
        

    def _set_render_properties(self, freestanding=False):
        
        self._num = get_joogle_object_counter()
        if self._label:
            self._name = self._label + FILTER_NAME_ADD_ON
            self._global_name = True
        else:
            self._name = "google_filter_" + str(self._num)
        self._div_id = self._name + "_div_id"
        
        # get data type, but only used for freestanding filters
        
        if freestanding:
            self.add_options(filterColumnIndex=0)
            if self._type == "CategoryFilter":
                self._data_type = "string"
            elif self._type == "DateRangeFilter":
                self._data_type = "date"
            elif self._type == "NumberRangeFilter":
                self._data_type = "number"
        
    def render(self, force_common=True, freestanding=True):
        
        self._set_render_properties(freestanding)
        context = {}
        context['callback_name'] = 'doStuff_' + str(self._num)
        context['filter'] = self
        
        set_common_on_context(context, force_common)
        
        return j2_env.get_template('top_freestanding_filter.html').render(context).encode('utf-8')


    def show(self, force_common=False):

        display(HTML(self.render(force_common)))

class SeriesFilter(_GoogleFilter):
    
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
        self._label = None
        self._global_name = False

    def add_options(self, options = None, **kwargs):
        
        message = "filter column is automatically set on a SeriesFilter"
        if options and (("filterColumnIndex" in options) or ("filterColumnLabel" in options)):
            raise JoogleChartsException(message)
        if kwargs.get("filterColumnIndex") or kwargs.get("filterColumnLabel"):
            raise JoogleChartsException(message)

        super(SeriesFilter, self).add_options(options, **kwargs) 

    def bind_filter(self, *args):
        
        message = "data is automatically bound on a SeriesFilter"
        raise JoogleChartsException(message)

    def set_filter_label(self, label):
        
        self._label = label

    def _set_render_properties(self, jooglechart):
        
        charts = jooglechart.charts
        view_cols = charts[0].view_cols

        # check if all charts have the same view cols
        if len(charts) > 1:
            charts = jooglechart.charts
            for chart in charts[1:]:
                if chart.view_cols != view_cols:
                    message = "For SeriesFilter, all charts must have the same view cols"
                    raise JoogleChartsException(message)
        
        
        try:
            columns = jooglechart._dataframe.columns.values.tolist()
        except:
            # TODO: data is in a 2d array
            columns = jooglechart._2d_array[0]
            
        # get a list of series column indices.
        # if view_cols is set, that will be our initial series index list
        # if not, take the indexes for all the columns
        if view_cols:
            series_indexes = view_cols[:]
        else:
            series_indexes = range(jooglechart._num_cols)

        # remove role cols from series indexes
        if jooglechart.roles:
            role_cols = [role[0] for role in jooglechart.roles]
            for col in role_cols:
                if col in series_indexes:
                    series_indexes.remove(col)
        
        # remove the category column -- first remaining series column
        series_indexes.pop(0)

        # get the series names
        series_names = [columns[ix] for ix in series_indexes]

        # make data frame of series names to use for series filter DataTable        
        df = pd.DataFrame({'columns': series_names})

        # default selectedValues to all
        if not self._state.get('selectedValues'):
            self._state['selectedValues'] = series_names

        self._filter_table_json = dataframe_to_gviz(df).ToJSon()
        self._series_indexes = series_indexes
        self._num = get_joogle_object_counter()
        
        if self._label:
            self._name = self._label + FILTER_NAME_ADD_ON
            self._global_name = True
        else:
            self._name = "google_filter_" + str(self._num)
                    
        self._div_id = self._name + "_div_id"

class SuperCategoryFilter(_GoogleFilter):

    show_child_filters = False
        
    def __init__(self, choices, show_child_filters=False):
        
        super(SuperCategoryFilter, self).__init__(None)
#         Filter.__init__(self, None)
        self.add_options(ui_label = "Options")
        self.add_options(filterColumnIndex = 0)

        self._filter_labels = []
        self.show_child_filters = show_child_filters
        
        try:
            if isinstance(choices, pd.Series):
                pass
            else:
                choices = pd.Series(choices)
        except:
            message = "SuperCategoryFilter options must be a pandas Series or list"
            raise JoogleChartsException(message)
        choices.name = "options"
        df = pd.DataFrame(choices, columns=['options'])
        table = dataframe_to_gviz(df)
        self._json = table.ToJSon()


    
    def add_filter_label(self, filter_label):
        self._filter_labels.append(filter_label)

    def _set_render_properties(self):
        
        # set name, div id, data name, bound filter names
        self._num = get_joogle_object_counter()
        self._name = "super_category_filter_" + str(self._num)
        self._div_id = self._name + "_div_id"
        self._filter_names = [name + FILTER_NAME_ADD_ON for name in self._filter_labels]
    
    def render(self, force_common=True):
        
        self._set_render_properties()
        context = {}
        context['callback_name'] = 'doStuff_' + str(self._num)
        context['super_filter'] = self
        context['super_filter_type'] = 'category'
    
        # ISHBOOK-495
#         context['notebook_url'] = _get_notebook_url()

        set_common_on_context(context, force_common)
        
        return j2_env.get_template('super_filter_template.html').render(context).encode('utf-8')


    def show(self, force_common=False):

        display(HTML(self.render(force_common)))




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
                raise JoogleChartsException(message)

        type = self.FORMATTER_TYPES[formatter_ix]

        if type == "ColorFormat":
            message = "ColorFormat is not currently supported"
            raise JoogleChartsException(message)


        if type == 'PatternFormat':
            if source_cols is None or pattern is None:
                message = "PatternFormat requires source_cols and pattern"
                raise JoogleChartsException(message)
        elif cols is None or options is None:
            message = "This format requires options and cols"
            raise JoogleChartsException(message)


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

        self.num = get_joogle_object_counter()
        self.name = "formatter" + str(self.num)




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
        self._div_classes = []
        self._senders = []

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

    def add_div_class(self, _class):
        
        if _class == None:
            self._div_classes = []
        else:
            self._div_classes.append(_class)

    def set_view_cols(self, cols):

        if isinstance(cols, int):
            cols = [cols]
        self.view_cols = cols

    def add_sender(self, key, on="select", type='send_selection'):
        # possible types:
        #   send date range
        #   send number range
        
        self._senders.append({'on': on, 'key': key, 'type': type})

    def _set_render_properties(self, num_cols, chart_type=None):

        # chart render properties
        self.num = get_joogle_object_counter()
        self.name = "google_chart_" + str(self.num)
        self.chart_div_id = self.name + "_div_id"

        # set chart options to empty dict if it's been nulled out
        if self.chart_options == None:
            self.chart_options = {}


        # add default classes
        self.add_div_class("jooglechart_container")
#         self._div_classes.append("jooglechart_container")        
        chart_type_class = "jooglechart_type_" + self.chart_type
        self.add_div_class(chart_type_class)
#         self._div_classes.append(chart_type_class)


        # set chart type to display
        if chart_type == None:
            self.display_chart_type = self.chart_type
        else:
            self.display_chart_type = chart_type

class Styler():
    
    def apply_styles(self, chart):
        raise NotImplementedError('subclasses must override apply_styles()!')
        

class JoogleChart():

    # TODO:  add handling of view cols as names rather than indexes.    

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
        self._stylers = []
        self._num_cols = None
        self._num_rows = None
        self._global_title = None
        self._has_senders = False

        # Dashboard attributes
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

                df = pd.DataFrame(args[0])
                for s in args[1:]:
                    df[s.name] = s

            except:
                message = "Data must be passed as 2d array, a DataFrame, or 2 or more Series"
                raise JoogleChartsException(message)
            self._dataframe = df
            table = dataframe_to_gviz(df, datetime_cols=self.datetime_cols, allow_nulls=self.allow_nulls)
            self.json = table.ToJSon()


        if self._2d_array:
            self._num_cols = len(self._2d_array[0])
            self._num_rows = len(self._2d_array) - 1  #minus one for header row
        else:
            self._num_cols = len(self._dataframe.columns)
            self._num_rows = len(self._dataframe)
            

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

    def _add_series_filter(self, filter):
        
        self._series_filter = filter

    def set_role(self, col, role):

        if self.roles == None:
            self.roles = []
        if not col and not role:
            message = "col and role are required parameters."
            raise JoogleChartsException(message)

        self.roles.append((col, role))

    def set_tooltip(self, col, html=False):
        self.set_role(col, 'tooltip')
        self.tooltip_html = html

    def add_div_styles(self, *args, **kwargs):

        self.charts[0].add_div_styles(*args, **kwargs)
        
    def add_div_class(self, _class):
        
        self.charts[0].add_div_class(_class)

    def add_styler(self, styler):
        
        self._stylers.append(styler)

    def add_global_title(self, title):
        
        self._global_title = title

    def _add_chart(self, chart):
        self.charts.append(chart)

    def copy(self):

        return copy.deepcopy(self)

    def add_sender(self, key, on="select", type='send_selection'):
        # possible types:
        #   send date range
        #   send number range
        
        self._has_senders = True
        self.charts[0].add_sender(key, on, type)
#         self._senders.append({'on': on, 'key': key, 'type': type})

    def _set_render_properties(self, chart_type=None):

        """
        Set values needed for rendering the chart
        """


        # jg render properties
        self.num = get_joogle_object_counter()
        self.name = "jooglechart_" + str(self.num)
        self.data_name = self.name + "_data"
        self.view_name = self.name + "_view"
        self.dashboard_name = self.name + "_dashboard"
        self.dashboard_div_id = self.dashboard_name + "_div_id"

        for styler in self._stylers:
            styler(self)            

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
            num_cols = len(self._2d_array[0])

        # get the number of columns
        for index, chart in enumerate(self.charts):
            if index == 0:
                chart._set_render_properties(num_cols, chart_type)
            else:
                chart._set_render_properties(num_cols)

        # set render properties for filters
        for filter_ in self.filters:
            filter_._set_render_properties()

        # set render properties for series filter
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


    def render(self, chart_type=None, force_common=True):

        """
        Render chart code.
        chart_type is one-off type; not saved to underlying chart.
        
        By default, DO force common for render()
        """
        self._set_render_properties(chart_type)
        
        context = {}
        context['jg'] = self
        context['callback_name'] = 'doStuff_' + str(self.num)

        # ISHBOOK-495
#         context['notebook_url'] = _get_notebook_url()
        
        set_common_on_context(context, force_common)
        
        return j2_env.get_template('chart_template.html').render(context).encode('utf-8')


    def show(self, chart_type=None, force_common=False, **kwargs):

        """
        .show creates chart with one-off chart type and style options.
        They aren't saved to the underlying chart.
        
        By default don't force common for show()
        """
        

        # any leftover kwargs are assumed to be chart options
        chart = self.copy()
        if kwargs:
            chart.add_chart_options(**kwargs)
        else:
            chart = self
        display(HTML(chart.render(chart_type, force_common)))


class ChartRow:

    """
    A ChartRow can create a row of charts to display side-by-side.  Currently,
    The charts are rendered in 2-4 bootstrap columns of equal size.

    Pass 2-4 chart objects to the constructor.
    """

    def __init__(self, *jcs):

        self.jcs = jcs
        self.num_jcs = len(self.jcs)

        if self.num_jcs not in [2, 3, 4]:
            message = "A chart row must have 2-4 charts"
            raise JoogleChartsException(message)

        self.bootstrap_num = 12 / self.num_jcs



    def render(self, force_common=True):

        self.num = get_joogle_object_counter()

        for jc in self.jcs:
            jc._set_render_properties()

        context = {}
        context['chartrow'] = self
        context['callback_name'] = 'doStuff_' + str(self.num)

        # ISHBOOK-495
#         context['notebook_url'] = _get_notebook_url()

        set_common_on_context(context, force_common)

        return j2_env.get_template('chartrow_template.html').render(context).encode('utf-8')

    def show(self, force_common=False):

        display(HTML(self.render(force_common)))



def _gplot(self, chart_type=None, **kwargs):

    chart = JoogleChart(self)
    if kwargs:
        chart.add_chart_options(kwargs)
    chart.show(chart_type)

pd.DataFrame.gplot = _gplot
