#!/usr/bin/env python
# -*- coding: utf-8 -*-

from api import *
from globs import *
from utils import _pretty

if __name__=="__main__":
    if DEBUG:
        getTopStories("title")
