'''
Created on Dec 24, 2015

@author: richd
'''

from datetime import datetime, date

import pandas as pd

import json

# The js wrappers are characters to place at the beginning and end of a string
# for the purpose of deleting the quotation marks that appear at the beginning and 
# end of strings after going through json.dumps.  This is so a string can be put in the 
# jinja template as raw javascript, not a string value in quotes.

# Raw javascript is needed for the Date constructor in the DataTable.  Also,
# a user may wrap a string with the wrappers if they want it to be included as
# raw javascript in the jooglechart.  For example, tooltips in a Tree Map are created
# with javascript functions, which need to be passed as raw javascript.

js_wrapper_left = "|"
js_wrapper_right = "|"

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        
        if isinstance(obj, datetime):
            wrapped = js_wrapper_left + "new Date({}, {}, {}, {}, {}, {})" + js_wrapper_right 
            return wrapped.format(obj.year, obj.month - 1, obj.day,
                                obj.hour, obj.minute, obj.second)
        if isinstance(obj, date):
            wrapped = js_wrapper_left + "new Date({}, {}, {})" + js_wrapper_right 
            return wrapped.format(obj.year, obj.month - 1, obj.day)
        
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def to_json(d):
    out = json.dumps(d, cls=DateEncoder)
    out = out.replace(js_wrapper_right + '"', '')
    out = out.replace('"' + js_wrapper_left, '')
    
    # get rid of literal "\n" added by json.dumps and replace with newline.
    out = out.replace("\\n", "\n" )
    
    # get rid of escaping the may be added by json.dumps
    out = out.replace('\\"', '"' )
    
    return out


def format_styles_list(div_styles):

    if div_styles:
        style_base = "%s: %s"
        style_list = []
        for k, v in div_styles.iteritems():
            style_list.append(style_base % (k, v))
        return 'style="%s"' % "; ".join(style_list)
    else:
        return ""
    
def get_classes(class_list):
    
    if class_list:
        
        return 'class="%s"' % " ".join(class_list)
    
    else:
        return ""


# s = """|
#   function showStaticTooltip(row, size, value) {
#     return '<div style="background:#fd9; padding:10px; border-style:solid">' +
#            'Read more about the <a href="http://en.wikipedia.org/wiki/Kingdom_(biology)">kingdoms of life</a>.</div>';
#   }
# |"""
# print to_json(s)