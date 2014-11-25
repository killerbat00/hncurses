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

    def _makeURL(self,endpoint,id=None):
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

    def get_single(self,endpoint,id):
        '''
        Retrieves a single item or user from the API.


        Keyword arguemtns:
        endpoint -- API endpoint. Can be 'user' or 'item'
        id       -- ID of item/user
        '''
        url = self._makeURL(endpoint,id)
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

