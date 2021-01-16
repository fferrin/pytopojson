import numpy as np


class Array(object):
    def __init__(self, size=None):
        if size is not None:
            self.list = [0] * size
            self.size = size
        else:
            self.list = []
            self.size = 0

    def __getitem__(self, key):
        if isinstance(key, slice) or key < self.size:
            return self.list[key]
        else:
            return None

    def __setitem__(self, key, value):
        if key < self.size:
            self.list[key] = self._convert(value)

    def __len__(self):
        return self.size

    def __repr__(self):
        return "{classname}({list_obj})".format(
            classname=self.__class__.__name__, list_obj=self.list.__repr__()
        )

    def __str__(self):
        return "{classname}({list_obj})".format(
            classname=self.__class__.__name__, list_obj=self.list.__str__()
        )

    @staticmethod
    def _convert(value):
        return value


class Int8Array(Array):
    def __init__(self, size=None):
        super(Int8Array, self).__init__(size)

    @staticmethod
    def _convert(value):
        return np.array([value]).astype(np.int8)[0]


class Int16Array(Array):
    def __init__(self, size=None):
        super(Int16Array, self).__init__(size)

    @staticmethod
    def _convert(value):
        return np.array([value]).astype(np.int16)[0]


class Int32Array(Array):
    def __init__(self, size=None):
        super(Int32Array, self).__init__(size)

    @staticmethod
    def _convert(value):
        return np.array([value]).astype(np.int32)[0]


class ListDict(dict):
    def __init__(self, *args, **kw):
        super(ListDict, self).__init__(*args, **kw)

    def keys(self):
        return sorted(list(super(ListDict, self).keys()))

    def values(self):
        vals = list()
        for k in self.keys():
            vals.append(self[k])
        return vals

    def append(self, value):
        k = len(self.keys())
        self[k] = value

    def __delitem__(self, key):
        value = super().pop(key)
        super().pop(value, None)

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        super().__setitem__(key, value)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        try:
            x = self[self.index]
        except KeyError:
            raise StopIteration
        self.index += 1
        return x

    def __str__(self):
        return str(self.values())

    def __unicode__(self):
        return str(self.values())

    def __repr__(self):
        return str(self.values())

    def to_list(self):
        return self.values()


if __name__ == "__main__":
    a = Int8Array(5)
    print(a)
    a[3] = 2387
    print(a)
    a[10] = 10
    print(a)

    a = ListDict({0: 1, 1: 2})
    a.append(123)
    print(a)
