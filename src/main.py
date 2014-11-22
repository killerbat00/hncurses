#!/usr/bin/env python
# -*- coding: utf-8 -*-

from api import *
from globs import *
from utils import _pretty,_dircheck,_filecheck

def init():
    _dircheck()
    _filecheck()

if __name__=="__main__":
    init()
    if DEBUG:
        getTopStories("title")
