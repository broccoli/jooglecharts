'''
Created on Dec 24, 2015

@author: richd
'''

from datetime import datetime, date

import pandas as pd

import json

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return "|new Date({}, {}, {}, {}, {}, {})|".format(obj.year, obj.month - 1, obj.day,
                                obj.hour, obj.minute, obj.second)
        # Let the base class default method raise the TypeError
        if isinstance(obj, date):
            return "|new Date({}, {}, {})|".format(obj.year, obj.month - 1, obj.day)
        return json.JSONEncoder.default(self, obj)


def to_json(d):
    out = json.dumps(d, cls=DateEncoder)
    out = out.replace('|"', '')
    out = out.replace('"|', '')
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
