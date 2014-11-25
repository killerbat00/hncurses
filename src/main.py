#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hn import *
from config import DevConfig as config
from utils import _dircheck,_filecheck
import json

def init():
    '''
    Initialize requisite directories and files.
    '''
    _dircheck(config.FULL_DIR)
    _filecheck(config.CACHE_FILE)

if __name__=="__main__":
    init()
    hn = HN(config)
    for story in hn.get_frontpage():
        story = json.loads(story.rstrip())
        print story["title"] + "\t" + str(story["score"])

    print hn.max_item_id()
    print hn.get_updates()
