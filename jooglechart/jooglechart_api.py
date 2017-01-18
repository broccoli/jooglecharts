# -*- coding: utf-8 -*-

'''
Sonar todo:
-- NOT BROKEN.  fix daterange filter send/receive
-- DONE. change daterange filter send/receive to range for use by NumberRangeFilter
-- BACKBURNER.  Investigate button group bug when two button groups.  Happens when one bg controls a filter
  and another controls a chart.
-- DONE.  test standalone filters, make unit tests for category, date, number range
-- DONE.  make chart range receiver
-- DONE.  modify chart receiver to take column
-- WRAPS AROUND FINE.  test buttongroup wrap around when there are a lot of buttons
-- ADD BOLD, NOT COLOR.  add color option for button color.
-- DONE. add receive for checklist widget
-- DONE.  modify chartrow to accept widgets, text.
-- DONE.  test checklist widget for long lists.  Add height handling and scrollbars for long lists?
-- DONE. add titles to button group and checkbox group.
-- DONE.  create common code widget
-- DONE.  flexible widths in ChartRow; gutter in ChartRow
-- DONE.  ability to add div styles to all widgets and filters
-- DONE. add sender/receiver to SeriesFilter
-- DONE.  change include name to joogle_include
-- DONE. Change update chart to include view cols
-- DONE.  add update binding selection choices to filter handlers.  Must take binding column index.
-- DONE.  create clear button widget to clear other widgets
-- DONE.  chart with select freezes up when you click on legend.
-- DONE.  fix chart with select when you have a filter on it.
-- DONE.  SeriesFilter receivers and senders
-- DONE.  in filter receivers, check if div is in dom.
-- DONE.  Try setting initial values on stand alone filters
-- DONE. Add modes to chartrow.
-- NOT SONAR.  BACKBURNER. Add aggregation option to jooglechart?  Does an aggregation on a column.
-- DONE.  Figure out how to initialize charts and widgets that communicate with each other.
-- DONE.  Filter receiver doesn't work when sending/receiving empty selection.
-- DONE.  Add update_series receiver on charts for a series filter.
-- DONE.  Add message polling to filter receivers.
-- DONE.  Add DOM checking to filter receivers.
-- DONE.  Create get_visible_columns method for charts so that you can create a series filter.
-- DONE.  Add view_cols to update chart range.
-- DONE.  Change name of chart receiver actions.  filter_values, filter_range, filter_columns
-- DONE.  Change name of action for chart select?  DONE.  and type for sender. 
-- DONE.  Specify column for chart sender selection.  Need to specify column?  Yes I do.
-- DONE.  Custom legend.
-- DONE.  Specify button style as "button" or "link".  Need to check for these values in the widget.
-- DONE.  *** Add wrapping divs on all box items.
-- DONE.  change ButtonGroup parameter:  radio=True/False
    select_style = "single" "multi"
-- DONE.  Add check for message.data.msg is defined in window event listener.
-- DONE.  Remove initial_values from Legend.  Doesn't do anything different than values.
-- DONE.  change ChartRow padding to accept integer or string
-- DONE.  Change filter sender "type" to "message"
-- DONE.  Fix filter_columns when view_cols is set.
-- DONE.  make column not required for chart receiver (for filter_columns). make required for certain actions.
-- DONE.  check for unicode in Box and ChartRow



MINOR
-- Fix buttongroup send to buttongroup for radio
-- Add ButtonGroup, Button sizes:  small, medium, large
-- custom bound filter case:  select category, select city, unselect category. (city filter still shows but is not controlling)
    Check this behavior against real bound filter behavior.
-- when there's a range and category filter, range filtering doesn't check for category filtering.

MODERATE
-- text receiver widget. Much of it done, but don't know how to handle initial values, if initial values are lists for example.
-- ****** SeriesFilter doesn't work if you put a receiver on the chart.
-- change python viewable columns code for Series Filter.  Keep the names. Don't need in template.

ON HOLD
-- modify SuperCategoryFilter to use the sonar machinery behind the scenes?
-- *** Break supercategory filter if you put senders or receivers on it.
-- create Sender widget?  Sender just sends a value on load. (Can be used for testing.)
-- *** Add update binding range to filter handlers. Must take bound column index.
    This is for binding a category filter to a range filter
-- make checkboxGroup font size 12 pt.
-- Add Breakpoint parameter and @media max-height setting.
-- need a way to check if in aquarium for aquarium_hidden.
-- Add chart sender header, value
-- Add mouseover event for Legend.  Add mouseover sender to the api.


MAKE THEIR OWN TICKET
-- Change chart sender to sending col/row/all
-- CheckboxGroup -- make into class so it can trigger events, and add onetime listener.
    -- Also change from divs to list, and add title as a list item.
    -- Also add link/button option for clear button
-- Button -- make into class so it can trigger events, and add onetime listener and message polling
-- Create Widget class, make add_div_styles take underscore for hyphen.

UNIT TESTS, DEMOS
-- Create unit tests for connected filters/widgets that have initial values.
-- Create a detail chart demo using update selection.




styler todo
-- add indeed_colors=True option
-- accommodate bottom legend
-- parameter for right legend space




'''
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

from utils import get_joogle_object_counter, JoogleChartsException, _add_dict_to_dict, _validate_sender, joogle_include, _render_joogle_include
from dataframe_to_gviz import dataframe_to_gviz
from super_classes import ChartShow, ChartRender
from chart_filters import SeriesFilter, Filter, SuperCategoryFilter
from formatters import Formatter

from super_classes import AddDivStyles, ContainerRender


DEFAULT_CHART_TYPE = "ColumnChart"

# valid sonar messages and on events
VALID_CHART_MESSAGE_TYPES = {
    'category': ('select'),
    'agg': ('ready')                     
        }


class _Chart():

    def __init__(self, chart_type=None, **kwargs):

        # Chart attributes
        if chart_type == None:
            chart_type = DEFAULT_CHART_TYPE
        self.chart_type = chart_type
        self.display_chart_type = None
        self.chart_options = {}
        self.div_styles = {}
        self.view_cols = None
        self.chart_div_id = None
        self.num = None
        self.name = None
        self._div_classes = []
        self._senders = []
        self._receivers = []
        self._jooglechart = None
        self._visible_columns = None
        self._domain_column = None
        self._current_view_columns = None
        

 
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

        
    def add_sender(self, key, column=None, on="select", message_type='category'):

        _validate_sender(on, message_type, VALID_CHART_MESSAGE_TYPES)
        
        self._senders.append({'on': on, 'key': key, 'type': message_type, 'column': column})

    def add_receiver(self, key, *args, **kwargs):
        
        action = kwargs.pop('action', 'filter_values')
        
        column = kwargs.pop('column', None)
        
        if action in ['filter_values', 'filter_range'] and column is None:
            message = "A column must be specified in the chart receiver"
            message += " if the action is filter_values or filter_range"
            raise JoogleChartsException(message)
        
        receiver_dict = {}
        receiver_dict['key'] = key
        receiver_dict['action'] = action
        receiver_dict['column'] = column
        receiver_dict.update(kwargs)
        
        self._receivers.append(receiver_dict)
    
    def _get_viewable_series_indexes(self, exclude_filter_columns=False):
        
        # The viewable series are those charted in a line chart of bar chart, say.
        # They include the view cols, minus the domain column and the role columns.

        jooglechart = self._jooglechart
        
        # remove category column and role columns from visible columns
        if not self._visible_columns:
            self._set_visible_columns()
        series_indexes = self._visible_columns[:]
        
        if not self._domain_column:
            self._set_domain_column()
            
        series_indexes.remove(self._domain_column)
        for col in self._jooglechart._role_columns:
            series_indexes.remove(col)            
        
        # remove filter column indexes, if nec:
        if exclude_filter_columns:            
            for filter in jooglechart.filters:
                filter_column_index = filter._options.get("filterColumnIndex")
                series_indexes.remove(filter_column_index)


        return series_indexes
    

    def _set_visible_columns(self):
        # the visible columns are either the view_cols set by the user or all the column indexes.
        self._visible_columns = self.view_cols or range(self._jooglechart._num_cols)

    def _set_domain_column(self):
        # domain column is first visible non-role columns
        if self._jooglechart._role_columns:
            for col in self._visible_columns:
                if col not in self._jooglechart._role_columns:
                    self._domain_column = col
                    break
        else:
            self._domain_column = self._visible_columns[0]
        
        if self._domain_column is None:
            raise JoogleChartsException("A chart must have one visible non-role column")
        
    def _set_current_view_columns(self):
        
        self._current_view_columns = self.view_cols or None
        
    def _set_render_properties(self, chart_type=None, agg_chart=False):

        # chart render properties
        self.num = get_joogle_object_counter()
        self.name = "google_chart_" + str(self.num)
        self.chart_div_id = self.name + "_div_id"

        if not agg_chart:
            self._set_visible_columns()
            self._set_domain_column()
            self._set_current_view_columns()


        # set chart options to empty dict if it's been nulled out
        if self.chart_options == None:
            self.chart_options = {}

        # add default classes
        self.add_div_class("jooglechart_container")
        chart_type_class = "jooglechart_type_" + self.chart_type
        self.add_div_class(chart_type_class)


        # set chart type to display
        if chart_type == None:
            self.display_chart_type = self.chart_type
        else:
            self.display_chart_type = chart_type

        

class JoogleChart(ChartShow, ChartRender):

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
        self._role_columns = []
        self._global_title = None
        self._context_name = "jg"
        self._template = 'top_chart.html'
#         self._filter_layout = "auto"

        # Dashboard attributes
        self.dashboard_div_id = None

        # Chart attributes
        chart_type = kwargs.pop('chart_type', DEFAULT_CHART_TYPE)

#         self.charts.append(_Chart(chart_type))
        self._add_chart(_Chart(chart_type))

        # add any leftover kwargs to options
        if kwargs:
            self.charts[0].add_chart_options(**kwargs)


        self._set_data(args)
            

    def _set_data(self, args):
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

    
#     def _get_viewable_series_indexes_and_names(self):
# # 
#         return self.charts[0]._get_viewable_series_indexes_and_names()
    
    def _get_column_names(self, indexes):
        
        columns = None
        try:
            columns = self._dataframe.columns.values.tolist()
        except:
            columns = self._2d_array[0]
        
        # get the series names
        series_names = [columns[ix] for ix in indexes]
        
        return series_names
    
    def get_viewable_series(self, exclude_filter_columns=False):
        # Return the series names only.  Can be used to make a stand alone series filter
        # Return series for first chart.
        
        series_indexes = self.charts[0]._get_viewable_series_indexes(exclude_filter_columns=exclude_filter_columns)
        return self._get_column_names(series_indexes)

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
        self._role_columns.append(col)

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
        chart._jooglechart = self
        self.charts.append(chart)

    def copy(self):

        return copy.deepcopy(self)

    def add_sender(self, key, column=None, on="select", message_type='category'):
        # possible types:
        #   send date range
        #   send number range
        
        self.charts[0].add_sender(key, column, on, message_type)
#         self._senders.append({'on': on, 'key': key, 'type': type})


    def add_receiver(self, key, *args, **kwargs):
        # possible types:
        #   send date range
        #   send number range
        
        self._has_senders = True
        self.charts[0].add_receiver(key, **kwargs)
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

            # unicode            
            # Need to wrap the decoding in a try block so the user will be able to reshow
            # a chart in Jupyter.  If you reshow a chart, the code below will 
            # try to decode an already decoded string.         
            try:
                self.json = self.json.decode('utf-8')
            except UnicodeEncodeError:
                pass

        # render properties for charts
        for index, chart in enumerate(self.charts):
            if index == 0:
                chart._set_render_properties(chart_type)
            else:
                chart._set_render_properties()

        # set render properties for filters
        for filter_ in self.filters:
            filter_._set_render_properties()

        # set render properties for series filter (must be after charts)
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

        


class AggChart(ChartShow, ChartRender):

    def __init__(self, *args, **kwargs):
        
        
        self.num = None
        self._name = None
        self._chart = None
        self.formatters = []
        self._stylers = []
        self._global_title = None
        self._context_name = "agg_chart"
        self._template = 'top_agg_chart.html'
        self._div_id = None


        chart_type = kwargs.pop('chart_type', DEFAULT_CHART_TYPE)
        
        # make sure a dataframe or series wasn't passed in args or kwargs
        for i in list(args) + kwargs.values():
            if isinstance(i, (pd.DataFrame, pd.Series)):
                message = "AggChart does not accept DataFrames or Series"
                raise JoogleChartsException(message)

        self._chart = _Chart(chart_type)

        # adding chart to self.charts list so the bi styler can be used with AggChart
        self.charts = []
        self.charts.append(self._chart)
        


    def _unasable_function(self):
        message = "This function not available AggChart"
        raise JoogleChartsException(message)

    def add_chart_options(self, options=None, **kwargs):

        self._chart.add_chart_options(options, **kwargs)

    def set_view_cols(self, *args, **kwargs):
        self._unasable_function()

    def set_chart_type(self, chart_type):
        self._charts.chart_type = chart_type

    def _get_column_names(self):
        self._unasable_function()
    
    def get_viewable_series(self):
        self._unasable_function()

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
        self._unasable_function()
        
    def _add_series_filter(self, filter):
        self._unasable_function()

    def set_role(self, col, role):
        self._unasable_function()

    def set_tooltip(self, col, html=False):
        self._unasable_function()

    def add_div_styles(self, *args, **kwargs):

        self._chart.add_div_styles(*args, **kwargs)
        
    def add_div_class(self, _class):
        
        self._chart.add_div_class(_class)

    def add_styler(self, styler):
        
        self._stylers.append(styler)

    def add_global_title(self, title):
        
        self._global_title = title

    def _add_chart(self, chart):
        self._unasable_function()

    def copy(self):
        self._unasable_function()

    def add_sender(self, key, column, on="select", message_type='category'):
        
        self._chart.add_sender(key, column, on, message_type)

    def add_receiver(self, key, **kwargs):

        # An aggChart takes a to group on, and a column or columns to aggregate.
        # The aggregation columns require a column index, an agg function, and an optional label.
        # if a label is not specified, the function name is used.  agg_columns must be a list
        # dictionaries
        

        valid_agg_functions = ['avg', 'count', 'max', 'min', 'sum']
        
        group_column = kwargs.pop('group_column', None)
        if group_column is None:
            message = "A group column must be specified for an aggChart"
            raise JoogleChartsException(message)
        
        agg_columns = kwargs.pop('agg_columns', None)
        if agg_columns is None:
            message = "A list of agg columns must be specified for an aggChart"
            raise JoogleChartsException(message)
            
        
        # validate agg columns
        for agg_column in agg_columns:
            # An agg column must be a dictionary
            if not isinstance(agg_column, dict):
                message = "agg_columns must be a list of dictionaries"
                raise JoogleChartsException(message)
            if not 'column' in agg_column:
                message = "a column must be specified for each agg_column"
                raise JoogleChartsException(message)
            if not 'function' in agg_column:
                message = "a function must be specified for each agg_column"
                raise JoogleChartsException(message)
            if not 'label' in agg_column:
                agg_column['label'] = agg_column['function']
                        
        self._chart.add_receiver(key, action="aggregate_data", group_column=group_column, agg_columns=agg_columns)


    def _set_render_properties(self, chart_type=None):

        """
        Set values needed for rendering the chart
        """

        self.num = get_joogle_object_counter()
        self._name = "agg_chart_" + str(self.num)
        self._div_id = self._name + "_div_id"
        

        for styler in self._stylers:
            styler(self)            

        self._chart._set_render_properties(chart_type, agg_chart=True)



def _get_style_widths_from_weights(weights):
    
    # use less than 100 in case the computed widths in pixels are fractional and get rounded up,
    # potentially exceeding 100 total.
    TOTAL_WIDTH = 99
    weight_sum = sum(weights)
    style_widths = []
    for weight in weights:
        pct = (float(weight) / weight_sum) * TOTAL_WIDTH
        pct = round(pct, 2)
        style_width = 'style="width:{}%"'.format(pct)
        style_widths.append(style_width)
    return style_widths

class ChartRow(AddDivStyles, ContainerRender):

    """
    A ChartRow can create a row of charts to display side-by-side.  Currently,
    The charts are rendered in 2-4 bootstrap columns of equal size.

    Pass 2-4 chart objects to the constructor.
    """
    
    """
    There should be four ChartRow sizing modes:
        -- bootstrap
            -- evenly proportioned, but fixed width and responsive
        -- free
            no width setting
        -- weighted
            percent widths
        -- exact (add?)
            px, em, etc.
            integers will be assumed to be pixels
            The width of the total shouldn't be set
        
    maybe have a setting for inner padding or gutter.  But the padding must
    be incorporated into the widths of the modes.  Padding + width must fit the
    overall width.
    
    Maybe have inner_pad just be an integer.  It will be pct or px depending on mode?

    Add border box.  I think with border box, I can have inner padding be either
    pct or px.
    
    Might want to change from 100% width to 99% width for weighted to make sure that
    fractional pixels rounding up doesn't throw off the layout.
    
    Setting for responsiveness breakpoint?
    
    """

    def __init__(self, *objects, **kwargs):

        self._objects = objects
        self.bootstrap_num = None
        self._content_strings = []
        self._div_id = None
        self._div_styles = None
        self._weights = []
        self._widths = []
        self._style_widths = []
        self._padding = None
        self._div_prefix = "joogle_chart_row"
        self._context_name = "chartrow"
        self._template = "top_chartrow.html"
        

        self._mode = kwargs.pop("mode", "bootstrap")
        if self._mode not in ['bootstrap', 'free', 'weighted', 'fixed']:
            message = "ChartRow mode must be bootstrap, free, weighted, or fixed."
            raise JoogleChartsException(message)
        
        
        padding = kwargs.pop("padding", None)
        
        if padding:
            try:
                # if it's an integer, add 'px'
                padding = int(padding)
                padding = str(padding) + "px"
            except:
                # if it's not an integer, just pass it verbaticm
                pass
            self._padding = padding
            
        self._weights = kwargs.pop("weights", [])
        if self._mode == "weighted":
            if not self._weights:
                message = "If using weighted mode, pass a list of weights to apply"
                raise JoogleChartsException(message)
            elif len(self._weights) != len(objects):
                message = "Numbers of objects and weights in a ChartRow must be the same."
                raise JoogleChartsException(message)
            else:
                self._style_widths = _get_style_widths_from_weights(self._weights)

        widths = kwargs.pop("widths", [])        
        if self._mode == "fixed":
            if not widths:
                message = "If using fixed mode, pass a list of widths to apply"
                raise JoogleChartsException(message)
            for width in widths:
                try:
                    # if it's an integer, add 'px'
                    w = int(width)
                    w = str(w) + "px"
                except:
                    # if it's not an integer, just pass it verbaticm
                    w = width
                self._style_widths.append('style="width:{}"'.format(w))

        if self._mode == "bootstrap":
            num_objects = len(self._objects)
            if num_objects not in [2, 3, 4]:
                message = "If using bootstrap mode, there can be 2-4 objects"
                raise JoogleChartsException(message)

            self.bootstrap_num = 12 / num_objects
        
        

    def show(self, include_common=None):

        display(HTML(self.render(include_common)))



def _gplot(self, chart_type=None, **kwargs):

    chart = JoogleChart(self)
    if kwargs:
        chart.add_chart_options(kwargs)
    chart.show(chart_type)

pd.DataFrame.gplot = _gplot
