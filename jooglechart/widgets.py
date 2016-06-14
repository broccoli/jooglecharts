'''
Created on Jun 12, 2016

@author: richd
'''

from utils import get_joogle_object_counter, set_common_on_context, j2_env

from IPython.display import display, HTML

import pandas as pd


class ButtonGroup(object):

    
    def __init__(self, values, initial_values=None, type="checkbox", 
            clear_button=False, clear_button_position="first",
            orientation="horizontal"):

        self._values = values
        self._initial_values = initial_values
        self._type = type
        self._clear_button = clear_button
        self._clear_button_position = clear_button_position
        self._orientation = orientation
        self._div_id = None
        self._senders = []
        self._receivers = []
    
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
            

    def add_sender(self, key):
        
        # For now, we assume the on event is click and the type of data sent
        # is the array of selections.  If that needs to change in the future,
        # add params on="click" and type="selection"
        
        self._senders.append({'key': key})
        
    
    def add_receiver(self, key):        
        
        # For now, we assume the action is updating selections.
        # If that needs to change, add param action="update_selections"
        
        self._receivers.append({'key': key})

    def render(self, force_common=True):
        
        self._set_render_properties()
        context = {}
        context['callback_name'] = 'doStuff_' + str(self._num)
        context['bg'] = self
        
        set_common_on_context(context, force_common)
        
        return j2_env.get_template('top_button_group.html').render(context).encode('utf-8')


    def show(self, force_common=False):

        display(HTML(self.render(force_common)))
    