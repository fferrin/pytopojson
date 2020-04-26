# -*- coding: utf-8 -*-

# Standard library imports

# Third-party imports

# Application-specific imports


class Bisect(object):
    def __init__(self):
        pass

    def __call__(self, a, x, *args, **kwargs):
        lo, hi = 0, len(a)

        while lo < hi:
            mid = lo + hi >> 1
            if a[mid] < x:
                lo = mid + 1
            else:
                hi = mid

        return lo
