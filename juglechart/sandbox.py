'''
Created on Dec 7, 2015

@author: richd
'''

from google_charts import PythonGoogleChartsException

chart_options = {}

def foo(options=None, **kwargs):
    
    def add_value_to_options(key_list, v):
    
        if len(key_list) == 1:
            chart_options[k] = v
        
        else:        
            new_option = {}
            obj = v
            for key in key_list[1:][::-1]:
                new_dict = {key:obj}
                obj = new_dict
                new_option[key_list[0]] = obj
                
            right_dict = new_option
            left_dict = chart_options
            go_on = True
            
            while go_on:
                
                for k, v in right_dict.iteritems():
                    
                    if not k in left_dict:
                        # if the k is not in the dict, it's new, so add it.
                        left_dict[k] = v
                        go_on = False
                        break
                    else:
                        # Throw an error if both values are not dicts, or if one is a dict
                        # and the other is not.  We don't know what do with these conflicts.
                        if ((not isinstance(left_dict[k], dict) and not isinstance(right_dict[k], dict))
                        or (isinstance(left_dict[k], dict) and not isinstance(right_dict[k], dict))
                        or (not isinstance(left_dict[k], dict) and isinstance(right_dict[k], dict))):
                            message = "The value submitted in {} conflicts with a previous value.".format(kwargs)
                            raise PythonGoogleChartsException(message)
                        else:
                            # now we know that both values are dicts.
    
                            # if k is in the dict and v is a dict,
                            # check if the next key in v on the right is in the next keys on the left
                            # if not, update the dict on the left.  We have a new
                            # dictionary value.
                            
                            right_keys = v.keys()
                            left_keys = left_dict[k].keys()
                            if not set(right_keys).issubset(set(left_keys)):
                                left_dict[k].update(v)
                                go_on = False
                                break
                            
                            # Here, the dictionary on the left continues the same chain
                            # as the left, to advance to the next value to look for a
                            # new dict value.
                            right_dict = v
                            left_dict = left_dict[k]
                            
    if options:
        
        for k, v in options.iteritems():
            k2 = k.replace('_', '.')
            key_list = k2.split(".")
            add_value_to_options(key_list, v)

    if kwargs:
        for k, v in kwargs.iteritems():
            key_list = k.split("_")
            add_value_to_options(key_list, v)
        
                
            
    
    print chart_options
"""
chart_options = {'a': {'b': {'c':7}}}
"""

opts = {'a.f': 5, 'a.c': 7, 'a.b.d': 3}

# foo(a=7)
# foo(a=8)
# foo(a_b_d=2, a_b_c=7)
# foo(opts, a_b_c=7)
foo(opts)
# foo(a_b_x=2)



