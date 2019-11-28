# -*- coding: utf-8 -*-

# Standard library imports

# Third-party imports

# Application-specific imports


class Identity(object):
    def __init__(self):
        pass

    def __call__(self, x, *args, **kwargs):
        return x
