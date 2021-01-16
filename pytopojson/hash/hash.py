import math

from pytopojson.commons import Array


class HashMap(object):
    def __init__(
        self, size, hash, equal, key_type=Array, key_empty=None, value_type=Array
    ):
        self.hash = hash
        self.equal = equal
        self.key_empty = key_empty
        self.size = 1 << max(4, int(math.ceil(math.log(size + 1e-9) / math.log(2))))
        self.key_store = key_type(self.size)
        self.val_store = value_type(self.size)
        self.mask = self.size - 1

        for i in range(self.size):
            self.key_store[i] = key_empty

        self.value = {
            "set": self.set,
            "maybeSet": self.maybe_set,
            "get": self.get,
            "keys": self.keys,
        }

    def set(self, key, value):
        index = self.hash(key) & self.mask
        match_key = self.key_store[index]
        collisions = 0

        while match_key != self.key_empty:
            if self.equal(match_key, key):
                self.val_store[index] = value
                return self.val_store[index]

            collisions += 1

            if self.size <= collisions:
                raise ValueError("Full HashMap")

            index = (index + 1) & self.mask
            match_key = self.key_store[index]

        self.key_store[index] = key
        self.val_store[index] = value
        return value

    def maybe_set(self, key, value):
        index = self.hash(key) & self.mask
        match_key = self.key_store[index]
        collisions = 1

        while match_key != self.key_empty:
            if self.equal(match_key, key):
                return self.val_store[index]

            collisions += 1
            if self.size <= collisions:
                raise ValueError("Full HashMap")

            index = (index + 1) & self.mask
            match_key = self.key_store[index]

        self.key_store[index] = key
        self.val_store[index] = value
        return value

    def get(self, key, missing_value=None):
        index = self.hash(key) & self.mask
        match_key = self.key_store[index]
        collisions = 1

        while match_key != self.key_empty:
            if self.equal(match_key, key):
                return self.val_store[index]
            if self.size <= collisions:
                break

            collisions += 1
            index = (index + 1) & self.mask
            match_key = self.key_store[index]

        return missing_value

    def keys(self):
        keys = list()
        i = 0
        n = len(self.key_store)

        # TODO: Check for k in self.key_store
        while i < n:
            match_key = self.key_store[i]
            if match_key != self.key_empty:
                keys.append(match_key)

        return keys


class HashSet(object):
    def __init__(self, size, hash, equal, type=Array, empty=None):
        self.size = 1 << max(4, int(math.ceil(math.log(size + 1e-9) / math.log(2))))
        self.hash = hash
        self.equal = equal
        self.empty = empty
        self.store = type(self.size)
        self.mask = self.size - 1

        for i in range(self.size):
            self.store[i] = empty

        self.value = {"add": self.add, "has": self.has, "values": self.values}

    def add(self, value):
        index = self.hash(value) & self.mask
        match = self.store[index]
        collisions = 0

        while match != self.empty:
            if self.equal(match, value):
                return True

            collisions += 1
            if self.size <= collisions:
                raise ValueError("Full hashset")

            index = (index + 1) & self.mask
            match = self.store[index]

        self.store[index] = value
        return True

    def has(self, value):
        index = self.hash(value) & self.mask
        match = self.store[index]
        collisions = 0

        while match != self.empty:
            if self.equal(match, value):
                return True

            collisions += 1
            if self.size <= collisions:
                break

            index = (index + 1) & self.mask
            match = self.store[index]

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
