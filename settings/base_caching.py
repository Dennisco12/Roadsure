#!/usr/bin/python3
""" BaseCaching module
"""

class BaseCaching():
    """ BaseCaching defines:
      - constants of the caching system
      - where the data are stored (in a dictionary)
    """
    MAX_ITEMS = 5

    def __init__(self):
        """ Initiliaze
        """
        self.cache_data = {}

    def require_cache(self, key, included_keys):
        """This returns true if a key needs to be cached
        """
        if key is None or included_keys is None:
            return True
        if included_keys == []:
            return True
        if key[-1] != '/':
            key += '/'
        if key in included_keys:
            return True
        else:
            return False

    def print_cache(self):
        """ Print the cache
        """
        print("Current cache:")
        for key in sorted(self.cache_data.keys()):
            print(key)

