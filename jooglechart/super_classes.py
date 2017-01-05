'''
Created on Sep 10, 2016

@author: richd
'''

from utils import get_joogle_object_counter, set_common_on_context, j2_env, _add_styles

from IPython.display import display, HTML

"""
MIXIN CLASSES

Mixin classes only provide common methods for subclasses.  They don't need
an __init__ method or instance variables.
"""

class AddDivStyles(object):
    
    """
    Mixin for dropping add_div_styles into Joogle objects
    """

    def add_div_styles(self, style_dict = None, **kwargs):        
        """
        pass styles for the chart div in a dictionary or as keyword arguments
        """
        _add_styles(self, "_div_styles", style_dict, **kwargs)
        


class ChartRender(object):
    def render(self, chart_type=None, include_common=None):

        """
        Render chart code.
        chart_type is one-off type; not saved to underlying chart.
        
        By default, DO force common for render()
        """
        self._set_render_properties(chart_type)
        
        context = {}
        context[self._context_name] = self
        context['callback_name'] = 'doStuff_' + str(self.num)

        set_common_on_context(context, include_common)
        
        return j2_env.get_template(self._template).render(context)
#         return j2_env.get_template(self._template).render(context).encode('utf-8')

class ContainerRender(object):

    """
    Mixin for dropping render function into Joogle containers.  This mixin checks
    properties of the object to perform different logic.
    
    The container object needs the following properties
        - self._context_name
        - either self._objects or self.content
    """
    
#     _first_toggler = True

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


        # check if we need to include the Toggler prototype
#         if self._context_name == "toggler":
#             if ContainerRender._first_toggler:
#                 ContainerRender._first_toggler = False
#                 context["include_toggler_prototype"] = True

#         out_string = j2_env.get_template(self._template).render(context)
#         try:
#             out_string = out_string.encode('utf-8')
#         except:
#             pass
 
#         return j2_env.get_template(self._template).render(context).encode('utf-8')
        return j2_env.get_template(self._template).render(context)
#         return out_string


class Show(object):

    """
    Mixin for dropping show function into Joogle objects
    """
    def show(self, include_common=True):

        display(HTML(self.render(include_common)))


class ChartShow(object):

    """
    Mixin for dropping show function into charts
    """
    def show(self, chart_type=None, include_common=None, **kwargs):

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
        display(HTML(chart.render(chart_type, include_common)))
