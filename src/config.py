# -*- coding: utf-8 -*-

from os.path import expanduser,join

class Config():
    '''
    Contains basic configuration directives.
    '''
    BASE_URL = "https://hacker-news.firebaseio.com"
    APP_VERSION = "0.5"
    VERSION = "v0"
    DEBUG = False
    EXPIRES_IN = 900

    HOME=expanduser("~")
    DIR=".hn"
    CACHE_FILENAME="hn-frontpage"
    FULL_DIR=join(HOME,DIR)
    CACHE_FILE=join(FULL_DIR,CACHE_FILENAME)
    MAX_WORKERS = 20

class TestConfig(Config):
    '''
    Overridden config directives specifically for testing.
    '''
    pass

class DevConfig(Config):
    '''
    Overridden config directives specifically for developing.
    '''
    DEBUG = True
