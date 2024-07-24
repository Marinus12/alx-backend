#!/usr/bin/python3
"""Module 4-mru_cache
Defines a MRUCache class that inherits from BaseCaching and implements
a MRU caching system.
"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """MRU caching system that inherits from BaseCaching."""

    def __init__(self):
        """Initialize the MRUCache instance."""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """Add an item to the cache.

        If the cache exceeds its limit discard the most recently used item MRU

        Args:
            key: The key of the item to add.
            item: The item to add to the cache.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.order.remove(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            mru_key = self.order.pop()
            del self.cache_data[mru_key]
            print(f"DISCARD: {mru_key}")

        self.cache_data[key] = item
        self.order.append(key)

    def get(self, key):
        """Retrieve an item from the cache.

        Args:
            key: The key of the item to retrieve.

        Returns:
            The value of the item if it exists, None otherwise.
        """
        if key is None or key not in self.cache_data:
            return None
        self.order.remove(key)
        self.order.append(key)
        return self.cache_data[key]
