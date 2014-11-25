#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import expanduser,join

class Config():
    ### API CONFIG ###
    BASE_URL = "https://hacker-news.firebaseio.com"
    VERSION = "v0"
    DEBUG = False
    EXPIRES_IN = 900


    ### GENERAL CONFIG ###
    HOME=expanduser("~")
    DIR=".hn"
    STORY_CACHE="top_story_full_cache"
    FULL_DIR=join(HOME,DIR)
    FULL_DIR_FILE=join(FULL_DIR,STORY_CACHE)

class TestConfig(Config):
    pass

class DevConfig(Config):
    Config.DEBUG = True
