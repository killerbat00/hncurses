#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

from utils import _makeURL,_cacheStories


LIVE_DATA = ["topstories", "maxitem", "updates"]

def getSingle(type=None,id=None):
    if id is None and type not in LIVE_DATA:
        return 'Err'
    if type:
        url = _makeURL(type) if type in LIVE_DATA else _makeURL(type,id)
    return requests.get(url).json()

def getTopStories(key):
    stories = getSingle("topstories")
    _cacheStories(stories)
#    for story in stories:
#        print getSingle("item",story)[key]
        
