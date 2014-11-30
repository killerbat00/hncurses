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
        baseurl  -- HN API URL.
        config   -- config object with various params related.
        '''
        self.config  = config
        self.baseurl = "/".join([self.config.BASE_URL, self.config.VERSION])
        self.session = FuturesSession(max_workers = config.MAX_WORKERS)

    def _make_URL(self, endpoint, id=None):
        '''
        Formats the URL with endpoint, id and json extension.

        Keyword arguments:
        endpoint -- API endpoint from which to retrieve data.
        id       -- ID of object to retrieve.
                    ID defaults to None if no argument is given.

        Returns:
        URL for specific object.
        '''
        arr = [self.baseurl, endpoint, str(id)] if id\
                else [self.baseurl, endpoint]

        return "/".join(arr) + ".json"

    def get_single(self, endpoint, id=None):
        '''
        Retrieves a single item or user from the API.

        Keyword arguments:
        endpoint -- API endpoint. Can be 'user' or 'item'
        id       -- ID of item/user

        Returns:
        JSON encoded result of all information from object.
        On error, returns the error.

        '''
        url  = self._make_URL(endpoint, id)
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

    def get_multi(self, endpoint, ids):
        '''
        Concurrently retrieve multiple objects from the API.
        Currently doesn't support retrieving mixed object types.

        Keyword arguments:
        endpoint -- URL endpoint of objects.
        ids      -- List of ids to retrieve.

        Returns:
        List of JSON encoded objects for each item.
        On error, returns List(err)

        '''
        res = map(self.session.get, [self._make_URL(endpoint, id) for id in ids])

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
        '''
        Helper function to retrieve the front page.
        This method checks against a timeout value
        to decide whether to load the cache or
        request new stories. It then retrieves the JSON 
        encoded story objects. Once the stories are
        retrieved, they're stored in the cache if necessary.
        TODO: Once further development is complete, we'll see if
        this method of getting the front page is the most efficient.

        Returns:
        List of JSON encoded story objects.
        '''
        from utils import _check_expired, _get_cache_file, _get_time

        stories   = []
        cachefile = self.config.CACHE_FILE

        if _check_expired(cachefile, self.config.EXPIRES_IN):
            storyList = self.get_single("topstories")
            stories   = map(json.dumps, self.get_multi("item", storyList))
            f = _get_cache_file(cachefile,"w")
            f.write(str(_get_time()) + "\n") #store cache-file creation time to check for expiration
            f.write("\n".join([x for x in stories])) #separate the stories with newline and write to file
            f.close()
        else:
            f = _get_cache_file(cachefile,"r")
            stories = f.readlines()
            f.close()

        return map(json.loads, [story.rstrip() for story in stories])

    def get_frontpage(self):
        '''
        Retrieve the HN frontpage. Currently, this uses an auxiliary 
        method that caches and then checks against a timeout value 
        to decide to load the cache or new stories. 
        TODO: Once further development is complete, we'll see if
        this method of getting the front page is the most efficient.

        Returns:
        List of JSON encoded story objects.
        '''
        return self._retrieve_stories()

    def get_max_item_id(self):
        '''
        Retrieve current max item ID.

        Returns:
        Max item ID.
        '''
        return int(self.get_single("maxitem"))

    def get_updates(self):
        '''
        Retrieve item and profile changes.

        Returns:
        JSON of items and profiles that have been recently updated.
        '''
        return self.get_single("updates")
