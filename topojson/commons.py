
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
        if key < self.size:
            return self.list[key]
        else:
            return None

    def __setitem__(self, key, value):
        if key < self.size:
            self.list[key] = self._convert(value)

    def __len__(self):
        return self.size

    def __repr__(self):
        return '{classname}({list_obj})'.format(classname=self.__class__.__name__, list_obj=self.list.__repr__())

    def __str__(self):
        return '{classname}({list_obj})'.format(classname=self.__class__.__name__, list_obj=self.list.__str__())

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


if __name__ == '__main__':
    a = Int8Array(5)
    print(a)
    a[3] = 2387
    print(a)
    a[10] = 10
    print(a)
