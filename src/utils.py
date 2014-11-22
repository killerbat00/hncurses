#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import time

from globs import *

def _getTime():
    return int(time.time())

def _pretty(jsonres):
    print json.dumps(jsonres,
            indent = 4, separators=(',', ': '))

def _makeURL(endpoint,id=None):
    arr = [BASE_URL,VERSION,endpoint,str(id)] if id\
            else [BASE_URL,VERSION,endpoint]
    return "/".join(arr)+".json"

def _popCache(stories,fh):
    fh.seek(0) #return to the beginning of file to write
    fh.write(str(_getTime())+ "\n")
    json.dump(stories,fh)
    

def _cacheStories(stories):
    home = os.path.expanduser("~")
    dirr = ".hn"
    filename = "story_cache"

    fulldir = os.path.join(home,dirr)
    fulldirfile = os.path.join(fulldir,filename)

    #using try/except prevents any race conditions
    try:
        os.makedirs(fulldir)
    except OSError:
        if not os.path.isdir(fulldir):
            raise

    if not os.path.isfile(fulldirfile):
        open(fulldirfile,"w").close()

    with open(fulldirfile,"r+") as f:
        line1 = f.readline()
        if line1 == "": #file hasn't been populated yet
            _popCache(stories,f)
        else:
            if int(line1.rstrip()) > _getTime() + EXPIRES_IN: #results expired, repopulate file
                _popCache(stories,f)
