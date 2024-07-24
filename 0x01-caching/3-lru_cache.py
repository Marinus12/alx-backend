#!/usr/bin/python3
"""Module 3-lru_cache
Defines a LRUCache class that inherits from BaseCaching and implements
a LRU caching system.
"""

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """LRU caching system that inherits from BaseCaching."""

    def __init__(self):
        """Initialize the LRUCache instance."""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """Add an item to the cache.

        If the cache exceeds its limit, discard least recently used item(LRU)

        Args:
            key: The key of the item to add.
            item: The item to add to the cache.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.order.remove(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            lru_key = self.order.pop(0)
            del self.cache_data[lru_key]
            print(f"DISCARD: {lru_key}")

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
