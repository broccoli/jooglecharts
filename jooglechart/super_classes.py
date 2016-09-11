'''
Created on Sep 10, 2016

@author: richd
'''

from utils import get_joogle_object_counter, set_common_on_context, j2_env, _add_styles
# from widgets import Toggler

from IPython.display import display, HTML

"""
Drop-in modules only provide common methods for subclasses.  They don't need
an __init__ method or instance variables.
"""
    

class AddDivStyles(object):
    
    """
    Module for dropping add_div_styles into Joogle objects
    """

    def add_div_styles(self, style_dict = None, **kwargs):        
        """
        pass styles for the chart div in a dictionary or as keyword arguments
        """
        _add_styles(self, "_div_styles", style_dict, **kwargs)
        


class ContainerRender(object):

    """
    Module for dropping render function into Joogle containers
    """
    
    _first_toggler = [True]

    def render(self, include_common=None):

        num = get_joogle_object_counter()
        self._div_id = self._div_prefix + str(num)

        context = {}
        context[self._context_name] = self
        context['callback_name'] = 'doStuff_' + str(num)

        # call common context method before rendering all child
        # objects
        set_common_on_context(context, include_common)

        if hasattr(self, "_objects"):
            # container takes multiple objects
            for obj in self._objects:
                if isinstance(obj, (str, unicode)):
                    self._content_strings.append(obj)
                else:
                    self._content_strings.append(obj.render(include_common=False))
        elif hasattr(self, "_content"):
            # container takes one object
            if isinstance(self._content, (str, unicode)):
                self._content_string = self._content
            else:
                self._content_string = self._content.render(include_common=False)


        # check if we need to include the toggler prototype
        if self._context_name == "toggler":
            if ContainerRender._first_toggler:
                ContainerRender._first_toggler = False
                context["include_toggler_prototype"] = True


        return j2_env.get_template(self._template).render(context).encode('utf-8')

class Show(object):

    """
    Module for dropping show function into Joogle objects
    """
    def show(self, include_common=True):

        display(HTML(self.render(include_common)))
