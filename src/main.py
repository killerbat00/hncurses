#!/usr/bin/env python
# -*- coding: utf-8 -*-

from api2 import *
from config import DevConfig as config
from utils import _pretty,_dircheck,_filecheck

if __name__=="__main__":
    hn = HN(config)
    print hn.get_single("user","killerbat00")
