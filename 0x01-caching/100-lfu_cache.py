#!/usr/bin/python3
"""Module 100-lfu_cache
Defines an LFUCache class that inherits from BaseCaching and implements
a LFU caching system with LRU tie-breaking.
"""

from base_caching import BaseCaching
from collections import defaultdict, OrderedDict


class LFUCache(BaseCaching):
    """LFU caching system that inherits from BaseCaching."""

    def __init__(self):
        """Initialize the LFUCache instance."""
        super().__init__()
        self.key_freq = defaultdict(int)
        self.freq_keys = defaultdict(OrderedDict)
        self.min_freq = 0

    def _remove_least_frequent(self):
        """Remove the least frequently used item from the cache."""
        if not self.key_freq:
            return
        # Get the least frequent key
        least_freq_keys = self.freq_keys[self.min_freq]
        lru_key, _ = least_freq_keys.popitem(last=False)

        if not least_freq_keys:
            del self.freq_keys[self.min_freq]
        del self.cache_data[lru_key]
        del self.key_freq[lru_key]
        print(f"DISCARD: {lru_key}")

    def put(self, key, item):
        """Add an item to the cache.

        If the cache exceeds its limit, discard the least frequently used item
        and use LRU to break ties.

        Args:
            key: The key of the item to add.
            item: The item to add to the cache.
        """
        if key is None or item is None:
            return
        if key in self.cache_data:
            self.cache_data[key] = item
            self._update_freq(key)
            return
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            self._remove_least_frequent()
        self.cache_data[key] = item
        self.key_freq[key] = 1
        self.freq_keys[1][key] = item
        self.min_freq = 1

    def get(self, key):
        """Retrieve an item from the cache.

        Args:
            key: The key of the item to retrieve.

        Returns:
            The value of the item if it exists, None otherwise.
        """
        if key is None or key not in self.cache_data:
            return None
        self._update_freq(key)
        return self.cache_data[key]

    def _update_freq(self, key):
        """Update the frequency of an item.

        Args:
            key: The key of the item to update.
        """
        freq = self.key_freq[key]
        del self.freq_keys[freq][key]
        if not self.freq_keys[freq]:
            del self.freq_keys[freq]
            if freq == self.min_freq:
                self.min_freq += 1
        self.key_freq[key] += 1
        new_freq = self.key_freq[key]
        self.freq_keys[new_freq][key] = self.cache_data[key]
