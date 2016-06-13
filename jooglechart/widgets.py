'''
Created on Jun 12, 2016

@author: richd
'''

from utils import get_joogle_object_counter, set_common_on_context, j2_env

from IPython.display import display, HTML


class ButtonGroup(object):

    
    def __init__(self, values, initial_values=None, type="checkbox", 
            clear_button=False, clear_button_position="first",
            orientation="horizontal"):

        self.values = values
        self.initial_values = initial_values
        self.type = type
        self.clear_button = clear_button
        self.clear_button_position = clear_button_position
        self.orientation = orientation
        self._div_id = None
    
    def _set_render_properties(self, freestanding=False):
        
        self._num = get_joogle_object_counter()
        self._div_id = "button_group_" + str(self.num) + "_div_id"

    def render(self, force_common=True, freestanding=True):
        
        self._set_render_properties(freestanding)
        context = {}
        context['callback_name'] = 'doStuff_' + str(self._num)
        context['filter'] = self
        
        set_common_on_context(context, force_common)
        
        return j2_env.get_template('top_freestanding_filter.html').render(context).encode('utf-8')


    def show(self, force_common=False):

        display(HTML(self.render(force_common)))
    