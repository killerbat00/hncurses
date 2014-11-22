#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import expanduser,join

### API CONFIG ###
BASE_URL = "https://hacker-news.firebaseio.com"
VERSION = "v0"
DEBUG = True
EXPIRES_IN = 120


### GENERAL CONFIG ###
HOME=expanduser("~")
DIR=".hn"
STORY_CACHE="top_story_cache"
FULL_DIR=join(HOME,DIR)
FULL_DIR_FILE=join(FULL_DIR,STORY_CACHE)
