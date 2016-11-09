'''
Created on Nov 5, 2016

@author: richd
'''

from utils import (get_joogle_object_counter, set_common_on_context, j2_env, JoogleChartsException, _add_dict_to_dict,
    joogle_include, _render_joogle_include, _validate_sender)
import pandas as pd
from IPython.display import display, HTML
from dataframe_to_gviz import dataframe_to_gviz

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
        self._div_styles = {}
        self._has_selected_values = False

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

    def add_div_styles(self, style_dict = None, **kwargs):
        """
        pass styles for the chart div in a dictionary or as keyword arguments
        """

        if self._div_styles == None:
            self._div_styles = {}

        if style_dict == None and not kwargs:
            # user is resetting styles

            self._div_styles = {}
        else:
            if style_dict == None:
                style_dict = {}
            if kwargs:
                style_dict.update(kwargs)
            _add_dict_to_dict(self._div_styles, style_dict)
            

    def add_sender(self, key, on="statechange", message_type='default'):
        
        if message_type == "default":
            if self._type == "CategoryFilter":
                type = "values"
            elif self._type in ["DateRangeFilter", "NumberRangeFilter"]:
                type = "range"

                        
        self._senders.append({'on': on, 'key': key, 'type': type})
        
    
    def add_receiver(self, key, action="default", *args, **kwargs):

        rec_dict = {}
        if action == "default":
            if self._type == "CategoryFilter":
                action = "update_values"
            elif self._type in ["DateRangeFilter", "NumberRangeFilter"]:
                action = "update_range"
        
        if action == "update_binding_values":
            if "bound_column" in kwargs:
                rec_dict['bound_column'] = kwargs['bound_column']
            else:
                raise JoogleChartsException("A bound_column must be passed for update_binding_selection")
        rec_dict['key'] = key
        rec_dict['action'] = action
        
        self._receivers.append(rec_dict)

    def _set_render_properties(self):
        raise JoogleChartsException("_set_render_properties not implemented")
        


class Filter(_GoogleFilter):

    """
    filter object that you pass to a chart object.
    By default binds the data.  But can bind another filter.
    """

    def __init__(self, type, *args, **kwargs):
        super(Filter, self).__init__(type)
        self._label = None
        self._json = None
        self._data_type = None
        self._data = None
        self._filter_column_index = None
        self._series_names = None
        
        if 'data' in kwargs:
            self._data = kwargs['data']
            if not (isinstance(self._data, pd.Series) or isinstance(self._data, pd.DataFrame)):
                raise JoogleChartsException("Filter data must be Series or DataFrame")
            if isinstance(self._data, pd.Series):
                if self._data.name == None:
                    self._data.name = "choices"
                df = pd.DataFrame(self._data)
            else:
                df = self._data
            table = dataframe_to_gviz(df, allow_nulls=True)
            self._json = table.ToJSon()

    def bind_filter(self, bind_target):
        self._bind_target = bind_target
        
        if isinstance(bind_target, SeriesFilter):
            message = "Cannot bind a SeriesFilter"
            raise JoogleChartsException(message)

    def set_filter_label(self, label):
        
        # deprecated function for super category filter target
        
        self._label = label
        

    def _set_render_properties(self, freestanding=False):
        
        self._num = get_joogle_object_counter()
        if self._label:
            self._name = self._label + FILTER_NAME_ADD_ON
            self._global_name = True
        else:
            self._name = "google_filter_" + str(self._num)
        self._div_id = self._name + "_div_id"
        
        # get data type, but only used for freestanding filters
        
        if freestanding and not "filterColumnIndex" in self._options:
            raise JoogleChartsException("Standalone filter must have filterColumnIndex")
        else:
            self._filter_column_index = self._options['filterColumnIndex']
            
        
#         print self._filter_column_index
#         print isinstance(self._data, pd.DataFrame)
#         print self._data
        
        if freestanding:
            if isinstance(self._data, pd.DataFrame):
                self._series_names = list(self._data.ix[:, self._filter_column_index].values)
            else:
                self._series_names = list(self._data.values)
#         self._series_names = self._data.iloc[0].values
#         self._series_names = self._data.ix[:, self._filter_column_index].values

        # get has_selected_values to see if a one time ready listener is needed.
        self._has_selected_values = 'selectedValues' in self._state
        
        
    def render(self, include_common=None, freestanding=True):
        
        
        self._set_render_properties(freestanding)
        context = {}
        context['callback_name'] = 'doStuff_' + str(self._num)
        context['filter'] = self
        
        set_common_on_context(context, include_common)
        
        return j2_env.get_template('top_freestanding_filter.html').render(context).encode('utf-8')


    def show(self, include_common=None):

        display(HTML(self.render(include_common)))

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
        super(SeriesFilter, self).__init__("CategoryFilter")
#         Filter.__init__(self, None)
        self.add_options(ui_label = "Columns")
        self.add_options(filterColumnIndex = 0)
        self._label = None
        self._global_name = False
        self._series_names = None

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
                
        series_names = jooglechart.get_viewable_series()
        
        self._series_names = series_names

        # make data frame of series names to use for series filter DataTable        
        df = pd.DataFrame({'columns': series_names})

        # default selectedValues to all
        if not self._state.get('selectedValues'):
            self._state['selectedValues'] = series_names

        self._filter_table_json = dataframe_to_gviz(df).ToJSon()
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
    
    def render(self, include_common=None):
        
        self._set_render_properties()
        context = {}
        context['callback_name'] = 'doStuff_' + str(self._num)
        context['super_filter'] = self
        context['super_filter_type'] = 'category'
    
        set_common_on_context(context, include_common)
        
        return j2_env.get_template('super_filter_template.html').render(context).encode('utf-8')


    def show(self, include_common=None):

        display(HTML(self.render(include_common)))


