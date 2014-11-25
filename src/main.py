#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hn import *
from config import DevConfig as config
from utils import _dircheck,_filecheck

def init():
    _dircheck(config.FULL_DIR)
    _filecheck(config.CACHE_FILE)

if __name__=="__main__":
    init()
    hn = HN(config)
    hn.get_frontpage()
