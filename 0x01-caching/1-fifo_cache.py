#!/usr/bin/python3
""" A class FIFOCache that inherits from BaseCaching and is a cahcing system
   """
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """FIFO caching system that inherits from BaseCaching.
    Attributes:
        order (list): List to keep track of the order of insertion.
    """

    def __init__(self):
        """Inintialize the FIFOCache instance."""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """Add an item to the cache.

        If the cache exceeds its limit, discard, the first item added (FIFO)

        Args:
            key: The key of the item to add.
            item: The item to add to the cache.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.order.remove(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            first_key = self.order.pop(0)
            del self.cache_data[first_key]
            print(f"DISCARD: {first_key}")

        self.cache_data[key] = item
        self.order.append(key)

    def get(self, key):
        """Retrieve an item from cache.

        Args:
            key: The key of the item to retrieve.

        Returns:
            The calue of the item it it exists, None otherwise.
        """
        return self.cache_data.get(key)
