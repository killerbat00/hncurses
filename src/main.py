#!/usr/bin/env python
# -*- coding: utf-8 -*-

from api import *
from globs import *
from utils import _pretty

if __name__=="__main__":
    if DEBUG:
        _pretty(get("item",8863))
        _pretty(get("user","killerbat00"))
        _pretty(get("topstories"))
