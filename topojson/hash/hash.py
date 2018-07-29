import math


class HashMap(object):
    def __init__(self, size, hash, equal, key_type=list, key_empty=None, value_type=list):
        self.key_store = [None] * (1 << max(4, int(math.ceil(math.log(size) / math.log(2)))))
        self.val_store = [None] * size
        self.mask = size - 1

        for i in range(size):
            self.key_store[i] = key_empty

        self.value = {
            'set': None
        }

        def set(key, value):
            index = hash(key) & self.mask
            match_key = self.key_store[index]
            collisions = 0

            while match_key != key_empty:
                if match_key == key:
                    pass
                    # return self.val_store[index] = value


class HashSet(object):
    def __init__(self, size, hash, equal, type=list, empty=None):
        self.size = size
        self.empty = empty
        self.store = [None] * (1 << max(4, int(math.ceil(math.log(size) / math.log(2)))))
        self.mask = size - 1

        for i in range(size):
            self.store[i] = empty

        values = {
            'add': self.add,
            'has': self.has,
            'values': self.values
        }

    def add(self, value):
        index = hash(value) & self.mask
        match = self.store[index]
        collisions = 0

        while match != self.empty:
            if match == value:
                return True

            collisions += 1
            if self.size <= collisions:
                raise Exception("Full hashset")

            # match = self.store[index = (index + 1) & mask]

        self.store[index] = value
        return True

    def has(self, value):
        index = hash(value) & self.mask
        match = self.store[index]
        collisions = 0

        while match != self.empty:
            if match == value:
                return True

            collisions += 1
            if self.size <= collisions:
                break

            # match = self.store[index = (index + 1) & mask]

        return False

    def values(self):
        values = list()
        n = len(self.store)
        i = 0
        while i < n:
            match = self.store[i]
            if match != self.empty:
                values.append(match)

            i += 1

        return values



