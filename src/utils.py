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

### INIT ###
def _dircheck():
    try:
        os.makedirs(FULL_DIR)
    except OSError:
        if not os.path.isdir(FULL_DIR):
            raise

def _filecheck():
    if not os.path.isfile(FULL_DIR_FILE):
        open(FULL_DIR_FILE, "w").close()

### API ###
def _makeURL(endpoint,id=None):
    arr = [BASE_URL,VERSION,endpoint,str(id)] if id\
            else [BASE_URL,VERSION,endpoint]
    return "/".join(arr)+".json"

def _populateCache(stories):
    with open(FULL_DIR_FILE, "w") as fh:
        fh.write(str(_getTime())+ "\n")
        json.dump(stories,fh)
    
def _checkExpired():
    with open(FULL_DIR_FILE, "r") as fh:
        line1 = fh.readline().rstrip()
        return True if line1 == "" or int(line1) < _getTime() - EXPIRES_IN else False

def _topStoryFile():
    f = open(FULL_DIR_FILE, "r")
    f.readline()
    return f
