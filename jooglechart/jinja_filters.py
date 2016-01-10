'''
Created on Dec 24, 2015

@author: richd
'''

import json


def to_json(s):
    return json.dumps(s)


def format_styles_list(div_styles):

    if div_styles:
        style_base = "%s: %s"
        style_list = []
        for k, v in div_styles.iteritems():
            style_list.append(style_base % (k, v))
        return 'style="%s"' % "; ".join(style_list)
    else:
        return ""
