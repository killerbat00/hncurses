#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from globs import *

def _pretty(jsonres):
    print json.dumps(jsonres,
            indent = 4, separators=(',', ': '))

def _makeURL(endpoint,id=None):
    arr = [BASE_URL,VERSION,endpoint,str(id)] if id\
            else [BASE_URL,VERSION,endpoint]
    return "/".join(arr)+".json"
