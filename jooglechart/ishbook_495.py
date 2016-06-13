'''
Created on Jun 12, 2016

@author: richd
'''

import json

# ISHBOOK-495
BASE_NOTEBOOK_URL = "https://ishbook.corp.indeed.com/nb/{nbid}/dashboard/{qs}"

# ISHBOOK-495
def _is_real_ishbook(frame_globals):
    try:
        return "__nbparams__" in frame_globals
    except (KeyError, AttributeError):
        return False

# ISHBOOK-495
def _frame_globals():
    import inspect
    frame_globals = {}
    for frame in inspect.stack():
        if '__nbparams__' in frame[0].f_globals:
            return frame[0].f_globals
    return {}

# ISHBOOK-495
# Hack to get the notebook id if in the ishbook context.
def _get_nbid(frame_globals):
    ls_dict = frame_globals["__nbparams__"]["__meta__"]["lookup_service"]
    return json.loads(ls_dict["data"])["notebook"]

# ISHBOOK-495
# Hack to get the notebook params if in the ishbook context.
def _get_nbparams(frame_globals):
    params = frame_globals["__nbparams__"]
    return {k: v for (k, v) in params.iteritems() if k != "__meta__"}

# ISHBOOK-495
def _get_notebook_url():
    import urllib
    fg = _frame_globals()
    if _is_real_ishbook(fg):
        (nbid, nbparams) = (_get_nbid(fg), _get_nbparams(fg))
        qs = urllib.urlencode(nbparams, doseq=True)
        return BASE_NOTEBOOK_URL.format(nbid=nbid, qs=qs)
    else:
        return ''
