'''
Created on Jan 9, 2016

@author: richd
'''

import random 
import json
import os

from ishbook_495 import _get_notebook_url

import pandas as pd
import numpy as np

from IPython.display import display, HTML

from jinja2 import Environment, FileSystemLoader
from jinja_filters import to_json, format_styles_list, get_classes


x = ['a', 'b', 'c', 'd']
y = [4, 2, 5, 3]
d = {'x': x, 'y': y}
test_df = pd.DataFrame(d)


# Set up Jinja
PATH = os.path.dirname(os.path.abspath(__file__))
loader=FileSystemLoader(os.path.join(PATH, 'jinja_templates'))
j2_env = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
j2_env.filters['to_json'] = to_json
j2_env.filters['format_styles_list'] = format_styles_list
j2_env.filters['get_classes'] = get_classes


class JoogleChartsException(Exception):
    """ General exception object thrown by python google charts API """
    pass


### Keep a running counter for all instances of JugChart.
### The counter is appended to the div's id to insure that each id is unique
# chart_counter = [0]
# formatter_counter = [0]
# filter_counter = [0]
joogle_object_counter = [0]

def get_counter(counter_list):
    counter_list[0] += 1
    return counter_list[0]

def get_joogle_object_counter():
    return get_counter(joogle_object_counter)

is_first_joogle = [True]
def set_common_on_context(context, include_common):
    
    # I was loading common template only for the 
    # first jooglechart, but that causes a problems while
    # developing in Jupyter.  If the first jooglechart is
    # rerun, it won't have the common context, and if the output
    # is saved, a js error occurs on reload and no jooglechart
    # will run. (The document ready function won't run.)
    
    if include_common == None:
        if include_has_been_called[0]:
            context['common'] = False
        else:
            context['common'] = True
    else:
        if include_common:
            context['common'] = True
        else:
            context['common'] = False
        
    if is_first_joogle[0] == True:
        context['refresh_globals'] = True
        is_first_joogle[0] = False


    # I want to refresh the globals if either the first joogle object is run
    # or the joogle_include is run.
    
        
    # ISHBOOK-495
    context['notebook_url'] = _get_notebook_url()


include_has_been_called = [False]

def _render_joogle_include():
    
    include_has_been_called[0] = True
    
    context = {}
    context['callback_name'] = 'joogle_include'
    set_common_on_context(context, include_common=True)
    
    return j2_env.get_template('top_joogle_include.html').render(context).encode('utf-8')

def joogle_include():
    
    # joogle_include should be called before rendering any joogle object.  If
    # a joogle object is rendered first, problems can arise in development
    # if notebook cells are re-run.  This will cause the first object
    # to drop the common js code, and there will be a js error the next time
    # the notebook is open if the output is saved.
    
    display(HTML(_render_joogle_include()))

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


def get_random_int():

    pass

def sample_date_sequence(periods):
    
    rng = pd.date_range('1/1/2015', periods=periods, freq='D')

    return rng


def get_date_df(days=4, num_series=4):

    data = {}
    data['dates'] = sample_date_sequence(days)
    label_num = 65 # ascii 'A'
    
    columns = ['dates']
    
    for num in range(num_series):
        
        label = chr(label_num + num)
        mu = random.randint(20, 40)
        sd = 2
        s = np.random.normal(mu, sd, days)
        data[label] = s
        columns.append(label)

        
    return pd.DataFrame(data, columns=columns)



capitals = ['Sacramento', 'Montpelier', 'Juneau', 'Montgomery', 'Little Rock',
              'Phoenix', 'Denver', 'Hartford', 'Tallahassee', 'Dover', 'Atlanta', 'Honolulu',
           'Austin', 'Albany', 'Frankfurt', 'Topeka', 'Baton Rouge']

def get_df(rows=5, cols=1, min=20, max=100, category_column=False):
    random.seed(2)
    cities = capitals[:rows]
    d = {}
    columns = []
    d['cities'] = cities
    columns.append('cities')
    if category_column:
        categories = [chr(random.randint(65, 67)) for x in range(rows)]
        d['categories'] = categories
        columns.append('categories')
        
    for x in range(cols):
        name = chr(x + 65) + (chr(x + 97) * 8) # + chr(x + 97)
        data = [random.randint(min, max) for i in range(rows)]
        d[name] = data
        columns.append(name)
    return pd.DataFrame(d, columns=columns)

def replace_underscores_with_dashes(d):
    
    new_dict = {}
    
    for key in d:
        new_key = key.replace('_', '-')
        new_dict[new_key] = d[key]
    return new_dict


def _add_styles(obj, attr_name, style_dict, **kwargs):
    
    """
    Method for adding css styles to an object's style list.  The list can be an arbitrarily named list.
    Styles can be sent in a dictionary and/or in kwargs.  CSS styles with dashes
    can be sent in kwargs with underscores replacing dashes.
    """

    # check if the object has the attribute
    if not hasattr(obj, attr_name):
        message = "Object does not have the style list as attribute. Contact package developer."
        raise JoogleChartsException(message)
    
    # set None value to empty dictionary
    if getattr(obj, attr_name) == None:
        setattr(obj, attr_name, {})

    if style_dict == None and not kwargs:
        # user is resetting styles
        setattr(obj, attr_name, {})
    else:
        if style_dict == None:
            style_dict = {}
        if kwargs:
            kwargs = replace_underscores_with_dashes(kwargs)
            # combine style dict and kwargs into one dict
            style_dict.update(kwargs)
        _add_dict_to_dict(getattr(obj, attr_name), style_dict)
    

