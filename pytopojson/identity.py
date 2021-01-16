class Identity(object):
    def __init__(self):
        pass

    def __call__(self, x, *args, **kwargs):
        return x
