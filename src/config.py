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
    CACHE_FILENAME="hn-frontpage"
    FULL_DIR=join(HOME,DIR)
    CACHE_FILE=join(FULL_DIR,CACHE_FILENAME)
    MAX_WORKERS = 20

class TestConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
