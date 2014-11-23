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
    from utils import _checkExpired,_topStoryFile,_getTime
    from globs import FULL_DIR_FILE
    stories = []
    if _checkExpired():
        storyList = getSingle("topstories")
        f = _topStoryFile("w")
        f.write(str(_getTime()) + "\n")
        for story in storyList:
            s = json.dumps(getSingle("item", story))
            stories.append(s)
            f.write(s+"\n")
        f.close()
    else:
        f = _topStoryFile("r")
        stories = f.readlines()
        f.close()

    return stories

def getTopStories(key):
    for story in _retrieveStories():
        story = json.loads(story.rstrip())
        print story["title"] + "\t" + str(story["score"])
