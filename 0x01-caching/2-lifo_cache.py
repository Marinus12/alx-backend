#!/usr/bin/python3
"""A class LIFOCache that inherits from BaseCaching and is a caching system"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """LIFO caching system that inherits from BaseCaching."""

    def __init__(self):
        """Initializes the LIFOCache instance."""
        super().__init__()
        self.last_key = None

    def put(self, key, item):
        """Add an item to the cache.

        If the cache exceeds its limit, disard the last item added (LIFO)

        Args:
            key: The key of the item to add.
            item: The item to add to the cache.
        """
        if key is None or item is None:
            return

        if (len(self.cache_data) >= BaseCaching.MAX_ITEMS and
                key not in self.cache_data):
            if self.last_key is not None:
                del self.cache_data[self.last_key]
                print(f"DISCARD: {self.last_key}")

        self.cache_data[key] = item
        self.last_key = key

    def get(self, key):
        """Retrieve an item from te cache.

        Args:
            key: The key of the item to retrieve

        Returns:
            The value of the item if it exists, None otherwise.
        """
        return self.cache_data.get(key)
