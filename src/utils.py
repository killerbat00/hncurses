# -*- coding: utf-8 -*-

import json
import os
import time

from config import *

def _dircheck(hn_dir):
    '''
    Check for hn cache directory and create
    if it doesn't exist.

    Keyword arguments:
    hn_dir   -- Directory to store cache information.
    '''
    try:
        os.makedirs(hn_dir)
    except OSError:
        if not os.path.isdir(hn_dir):
            raise

def _filecheck(cachefile):
    '''
    Check for cache file, creating if non-existant.

    Keyword arguments:
    cachefile -- Filename for cache.
    '''
    if not os.path.isfile(cachefile):
        open(cachefile, "w").close()

def _make_URL(endpoint,id=None):
    '''
    Construct URL for json API request.

    Keyword arguments:
    endpoint -- URL endpoint to retrieve.
    id       -- ID of object to retrieve.
                Defaults to none to allow the retrieval
                of index items.
    Returns:
    URL for specific object.
    '''
    arr = [BASE_URL,VERSION,endpoint,str(id)] if id\
            else [BASE_URL,VERSION,endpoint]

    return "/".join(arr)+".json"

def _check_expired(cachefile,expiry):
    '''
    Check if the cache file is expired.

    Keyword arguments:
    cachefile -- Filename for cache.
    expiry    -- Number of seconds after which cache is expired.

    Returns:
    True if the cache is expired, False otherwise.
    '''
    with open(cachefile, "r") as fh:
        line1 = fh.readline().rstrip()

        return True if line1 == "" or int(line1) < _get_time() - expiry else False

def _get_cache_file(filename,mode):
    '''
    Open the cache file, throwing away the first line
    if we open in read mode. Doing so allows us to
    read the stories without worrying about accidentally getting cache file time.
    
    Keyword arguments:
    filename -- Cache filename.
    mode     -- Mode in which to open the file.

    Returns:
    File object for cache file.
    '''
    f = open(filename, mode)
    if mode == "r":
        f.readline()

    return f

def _get_time():
    '''
    Get current seconds since epoch as an int.

    Returns:
    int representation of seconds since epoch.
    ''' 
    return int(time.time())
