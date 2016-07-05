'''
Created on Jun 12, 2016

@author: richd
'''

from utils import get_joogle_object_counter, set_common_on_context, j2_env, _add_dict_to_dict, JoogleChartsException

from IPython.display import display, HTML

import pandas as pd


class ButtonGroup(object):

    
    def __init__(self, values, initial_values=None, type="checkbox", 
            clear_button=False, clear_button_position="first",
            orientation="horizontal", clear_button_bold=False, title=None):

        self._values = values
        self._initial_values = initial_values
        self._type = type
        self._clear_button = clear_button
        self._clear_button_position = clear_button_position
        self._orientation = orientation
        self._clear_button_bold = clear_button_bold
        self._div_id = None
        self._senders = []
        self._receivers = []
        self._div_styles = {}
        self._title = title
    
    def _set_render_properties(self):
        
        self._num = get_joogle_object_counter()
        self._div_id = "button_group_" + str(self._num) + "_div_id"
        
        if type(self._values) == pd.Series:
            self._values = self._values.tolist()
        
        if self._clear_button:
            self._clear_button = "true"
        else:
            self._clear_button = 'false'
            
        if self._clear_button_position == "last":
            self._append_or_prepend = "append"
        else:
            self._append_or_prepend = "prepend"
            
        if self._orientation == "vertical":
            self._button_group_class = "btn-group-vertical"
        else:
            self._button_group_class = "btn-group"
            
    def add_div_styles(self, style_dict = None, **kwargs):
        """
        pass styles for the chart div in a dictionary or as keyword arguments
        """

        if self._div_styles == None:
            self._div_styles = {}

        if style_dict == None and not kwargs:
            # user is resetting styles

            self.div_styles = {}
        else:
            if style_dict == None:
                style_dict = {}
            if kwargs:
                style_dict.update(kwargs)
            _add_dict_to_dict(self._div_styles, style_dict)
            

    def add_sender(self, key):
        
        # For now, we assume the on event is click and the type of data sent
        # is the array of selections.  If that needs to change in the future,
        # add params on="click" and type="selection"
        
        self._senders.append({'key': key})
        
    
    def add_receiver(self, key):        
        
        # For now, we assume the action is updating selections.
        # If that needs to change, add param action="update_selections"
        
        self._receivers.append({'key': key})

    def render(self, include_common=True):
        
        self._set_render_properties()
        context = {}
        context['callback_name'] = 'doStuff_' + str(self._num)
        context['bg'] = self
        
        set_common_on_context(context, include_common)
        
        return j2_env.get_template('top_button_group.html').render(context).encode('utf-8')


    def show(self, include_common=True):

        display(HTML(self.render(include_common)))
    
    

class CheckboxGroup(object):

    
    def __init__(self, values, initial_values=None, 
            clear_button=False, clear_button_position="first",
            orientation="vertical"):

        self._values = values
        self._initial_values = initial_values
        self._clear_button = clear_button
        self._clear_button_position = clear_button_position
        self._orientation = orientation
        self._div_id = None
        self._senders = []
        self._receivers = []
        self._div_styles = {}
    
    def _set_render_properties(self):
        
        self._num = get_joogle_object_counter()
        self._div_id = "checkbox_group_" + str(self._num) + "_div_id"
        
        if type(self._values) == pd.Series:
            self._values = self._values.tolist()
        
        if self._clear_button:
            self._clear_button = "true"
        else:
            self._clear_button = 'false'
            
        if self._clear_button_position == "last":
            self._append_or_prepend = "append"
        else:
            self._append_or_prepend = "prepend"
            

    def add_div_styles(self, style_dict = None, **kwargs):
        """
        pass styles for the chart div in a dictionary or as keyword arguments
        """

        if self._div_styles == None:
            self._div_styles = {}

        if style_dict == None and not kwargs:
            # user is resetting styles

            self.div_styles = {}
        else:
            if style_dict == None:
                style_dict = {}
            if kwargs:
                style_dict.update(kwargs)
            _add_dict_to_dict(self._div_styles, style_dict)
            

    def add_sender(self, key):
        
        # For now, we assume the on event is click and the type of data sent
        # is the array of selections.  If that needs to change in the future,
        # add params on="click" and type="selection"
        
        self._senders.append({'key': key})
        
    
    def add_receiver(self, key):        
        
        # For now, we assume the action is updating selections.
        # If that needs to change, add param action="update_selections"
        
        self._receivers.append({'key': key})

    def render(self, include_common=True):
        
        self._set_render_properties()
        context = {}
        context['callback_name'] = 'doStuff_' + str(self._num)
        context['cbg'] = self
        
        set_common_on_context(context, include_common)
        
        return j2_env.get_template('top_checkbox_group.html').render(context).encode('utf-8')


    def show(self, include_common=True):

        display(HTML(self.render(include_common)))
        
google_31 = ["#3366cc","#dc3912","#ff9900","#109618","#990099","#0099c6","#dd4477",
             "#66aa00","#b82e2e","#316395","#994499","#22aa99","#aaaa11","#6633cc",
             "#e67300","#8b0707","#651067","#329262","#5574a6","#3b3eac","#b77322",
             "#16d620","#b91383","#f4359e","#9c5935","#a9c413","#2a778d","#668d1c",
             "#bea413","#0c5922","#743411"]

indeed_20 = []


class TextReceiver(object):
    
    def __init__(self, key, text, array_style="parens", pretext=None, default=""):
        self._text = text
        self._pretext = pretext
        self._key = key
        self._array_style = array_style
        self._default = default

        if array_style not in ['parens', 'brackets', 'colloquial']:
            message = "TextReceiver array_style must be colloquial, parens, or brackets"
            raise JoogleChartsException(message)

        if self._pretext == None:
            self._pretext = text.replace(default)


    def render(self):
        
        context = {}
        context['text_receiver'] = self
        
        return j2_env.get_template('top_text_receiver.html').render(context).encode('utf-8')


    def show(self):

        display(HTML(self.render()))

def is_string(obj):
    try:
        dummy = unicode(obj)
        return True
        # string
    except:
        return False

class Button(object):

    def __init__(self, value, text, style="button"):

        self._value = None
        self._style = style
        self._text = text
        self._div_id = None
        self._senders = []
        self._receivers = []
        self._div_styles = {}
        
        # check if value is a string
        if is_string(value):
            value = value.strip()
            if len(value) == 0:
                value = []
            else:
                value = [value]
        elif value == None:
            value = []
        elif isinstance(value, list):
            pass
        else:
            raise JoogleChartsException("Button value must be string, list or None")
    
        self._value = value
    def _set_render_properties(self):
        
        self._num = get_joogle_object_counter()
        self._div_id = "joogle_button_" + str(self._num) + "_div_id"
                
        if self._style != "link":
            self._style = 'button'
                        

    def add_div_styles(self, style_dict = None, **kwargs):
        """
        pass styles for the chart div in a dictionary or as keyword arguments
        """

        if self._div_styles == None:
            self._div_styles = {}

        if style_dict == None and not kwargs:
            # user is resetting styles

            self.div_styles = {}
        else:
            if style_dict == None:
                style_dict = {}
            if kwargs:
                style_dict.update(kwargs)
            _add_dict_to_dict(self._div_styles, style_dict)
            

    def add_sender(self, key):
        
        # For now, we assume the on event is click and the type of data sent
        # is the array of selections.  If that needs to change in the future,
        # add params on="click" and type="selection"
        
        self._senders.append({'key': key})
        
    
    def add_receiver(self, key):        
        
        # For now, we assume the action is updating selections.
        # If that needs to change, add param action="update_selections"
        
        self._receivers.append({'key': key})

    def render(self, include_common=True):
        
        self._set_render_properties()
        context = {}
        context['callback_name'] = 'doStuff_' + str(self._num)
        context['button'] = self
        
        set_common_on_context(context, include_common)
        
        return j2_env.get_template('top_button.html').render(context).encode('utf-8')


    def show(self, include_common=True):

        display(HTML(self.render(include_common)))


class Box(object):
    
    def __init__(self, *objects, **kwargs):

        self._objects = objects
        self._content_strings = []
        self._div_styles = {}
        self._div_id = None
        self._display = kwargs.pop("display", "default")
        self._vertical_align = kwargs.pop("vertical_align", "default")

    def add_div_styles(self, style_dict = None, **kwargs):
        """
        pass styles for the chart div in a dictionary or as keyword arguments
        """

        if self._div_styles == None:
            self._div_styles = {}

        if style_dict == None and not kwargs:
            # user is resetting styles

            self.div_styles = {}
        else:
            if style_dict == None:
                style_dict = {}
            if kwargs:
                style_dict.update(kwargs)
            _add_dict_to_dict(self._div_styles, style_dict)

    def render(self, include_common=None):

        num = get_joogle_object_counter()
        self._div_id = "joogle_box_" + str(num)


        context = {}
        context['box'] = self
        context['callback_name'] = 'doStuff_' + str(num)

        # call common context method before rendering all child
        # objects
        set_common_on_context(context, include_common)

        for obj in self._objects:
            if isinstance(obj, str):
                self._content_strings.append(obj)
            else:
                self._content_strings.append(obj.render(include_common=False))


        return j2_env.get_template('top_box.html').render(context).encode('utf-8')

    def show(self, include_common=None):

        display(HTML(self.render(include_common)))

class TableLegend(object):
    
    
    def __init__(self, values, colors="google_31", initial_values=None):
        
        self._values = values
        self._initial_values = initial_values
        self._receivers = []
        self._div_id = None
        
        if colors == "google_31":
            self._colors = google_31
        else:
            self._colors = colors

    def add_receiver(self, key):
        
        # For now we assume the action is updating the legend keys
        # If things change we can add default param action="update_keys"

        self._receivers.append({'key': key})        


    def _set_render_properties(self):
        
        self._num = get_joogle_object_counter()
        self._div_id = "table_legend_" + str(self._num) + "_div_id"
    
    def render(self, include_common=True):
        
        self._set_render_properties()
        context = {}
        context['callback_name'] = 'doStuff_' + str(self._num)
        context['table_legend'] = self
        
        set_common_on_context(context, include_common)
        
        return j2_env.get_template('top_table_legend.html').render(context).encode('utf-8')
    
    def show(self, include_common=True):

        display(HTML(self.render(include_common)))
