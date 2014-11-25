#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests_futures.sessions import FuturesSession
import requests
from utils import *
import json


class HN():
    '''
    Base class for communicating with the HN API.
    '''

    def __init__(self, config):
        '''
        Sets up the requests session with the API.
        Use a FuturesSession as it provides support
        for concurrent requests.

        Keyword arguments:
        baseurl  -- HN API URL
        config   -- config object with various params related 
        '''
        self.config = config
        self.baseurl = "/".join([self.config.BASE_URL, self.config.VERSION])
        self.session = FuturesSession(max_workers=15)

    def _make_URL(self,endpoint,id=None):
        '''
        Formats the URL with endpoint, id and json extension.

        Keyword arguments:
        endpoint -- API endpoint from which to retrieve data
        id       -- ID of item/user to retrieve.
                    ID defaults to None if no argument is given.
        '''
        arr = [self.baseurl,endpoint,str(id)] if id\
                else [self.baseurl,endpoint]
        return "/".join(arr)+".json"

    def get_single(self,endpoint,id=None):
        '''
        Retrieves a single item or user from the API.


        Keyword arguments:
        endpoint -- API endpoint. Can be 'user' or 'item'
        id       -- ID of item/user
        '''
        url = self._make_URL(endpoint,id)
        resp = self.session.get(url)
        try:
            result = resp.result()
            result = result.json()
        except Exception as err:
            result = err
            if self.config.DEBUG:
                print type(err)
                print err.args
                print err
        return result

    def get_multi(self,endpoint,ids):
        '''
        Concurrently retrieve multiple objects from the API.
        Currently doesn't support retrieving mixed object types.

        Keyword arguments:
        endpoint -- URL endpoint of objects
        ids      -- List of ids to retrieve
        '''
        res = map(self.session.get, [self._make_URL(endpoint,id) for id in ids])
        try:
            results = [x.result().json() for x in res]
        except Exception as err:
            results = [err]
            if self.config.DEBUG:
                print type(err)
                print err.args
                print err
        return results

    def _retrieve_stories(self):
        from utils import _checkExpired, _cacheFile, _getTime
        stories = []
        cachefile = self.config.CACHE_FILE
        if _checkExpired(cachefile,self.config.EXPIRES_IN):
            storyList = self.get_single("topstories")
            f = _cacheFile(cachefile,"w")
            f.write(str(_getTime()) + "\n") #store cache-file creation time to check for expiration
            stories = map(json.dumps, self.get_multi("item",storyList))
            f.write("\n".join([x for x in stories])) #separate the stories with newline and write to file
            f.close()
        else:
            f = _cacheFile(cachefile,"r")
            stories = f.readlines()
            f.close()
        return stories

    def get_frontpage(self):
        '''
        Retrieve the HN frontpage. Currently, this uses an auxiliary 
        method that caches and then checks against a timeout value 
        to decide to load the cache or new stories. 
        TODO: Once further development is complete, we'll see if
        this method of getting the front page is the most efficient.
        '''
        for story in self._retrieve_stories():
            story = json.loads(story.rstrip())
            print story["title"] + "\t" + str(story["score"])
