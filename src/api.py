#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

LIVE_DATA = ["topstories", "maxitem", "updates"]

def getSingle(type=None,id=None):
    from utils import _makeURL
    if id is None and type not in LIVE_DATA:
        return 'Err'
    if type:
        url = _makeURL(type) if type in LIVE_DATA else _makeURL(type,id)
    return requests.get(url).json()

def _retrieveStories():
    from utils import _checkExpired,_populateCache,_topStoryFile
    stories = None
    if _checkExpired():
        stories = getSingle("topstories")
        _populateCache(stories)
    else:
        f = _topStoryFile()
        stories = json.load(f)
        f.close()

    return stories

def getTopStories(key):
    for story in _retrieveStories():
        print getSingle("item",story)[key]
