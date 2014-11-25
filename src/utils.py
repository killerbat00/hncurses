#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import time

from config import *

### INIT ###
def _dircheck(hn_dir):
    try:
        os.makedirs(hn_dir)
    except OSError:
        if not os.path.isdir(hn_dir):
            raise

def _filecheck(cachefile):
    if not os.path.isfile(cachefile):
        open(cachefile, "w").close()

### API ###
def _makeURL(endpoint,id=None):
    arr = [BASE_URL,VERSION,endpoint,str(id)] if id\
            else [BASE_URL,VERSION,endpoint]
    return "/".join(arr)+".json"

def _checkExpired(cachefile,expiry):
    with open(cachefile, "r") as fh:
        line1 = fh.readline().rstrip()
        return True if line1 == "" or int(line1) < _getTime() - expiry else False

def _cacheFile(filename,mode):
    f = open(filename, mode)
    if mode == "r":
        f.readline()
    return f

def _getTime():
    return int(time.time())

