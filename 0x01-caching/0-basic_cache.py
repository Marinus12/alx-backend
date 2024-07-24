#!/usr/bin/env python3
"""A class BasicCache that inherits from BaseCaching and is a caching system
   """
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """BasicCache defines a caching system with no limit"""
    def put(self, key, item):
        """Add an item in the cache"""
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """Get an item by key"""
        if key is None:
            return None
        return self.cache_data.get(key)
