from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        # initialize capacity and your OrderedDict here
        self.capacity= capacity
        self.cache = OrderedDict()

    def get(self, key):
        # if key doesn't exist return -1
        # otherwise move it to most recent end and return value
        if key not in self.cache:
            return -1
        else:
            self.cache.move_to_end(key)
            return self.cache[key]




    def put(self, key, value):
        # if key exists, update it and move to most recent end
        # if at capacity, remove least recent item
        # insert new key at most recent end
        if key in self.cache:
            self.cache[key] = value
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            # evict least recent
            self.cache.popitem(last=False)
            self.cache[key] = value
        else:
            self.cache[key] = value


cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))    # → 1
cache.put(3, 3)        # evicts key 2
print(cache.get(2))    # → -1
cache.put(4, 4)        # evicts key 1
print(cache.get(1))    # → -1
print(cache.get(3))    # → 3
print(cache.get(4))    # → 4