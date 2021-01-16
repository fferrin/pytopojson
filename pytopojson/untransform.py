from pytopojson import identity


class Untransform(object):
    def __init__(self):
        self.identity = identity.Identity()
        self.x_0 = 0
        self.y_0 = 0
        self.k_x = 0
        self.k_y = 0
        self.d_x = 0
        self.d_y = 0

    def __call__(self, transform=None, *args, **kwargs):
        if transform is None:
            return self.identity

        self.k_x, self.k_y = transform["scale"]
        self.d_x, self.d_y = transform["translate"]

        return self.func

    def func(self, input, i=None):
        if i is None or i == 0:
            self.x_0, self.y_0 = 0, 0
        output = input.copy()

        x_1 = int(round((input[0] - self.d_x) / self.k_x))
        y_1 = int(round((input[1] - self.d_y) / self.k_y))
        output[0] = x_1 - self.x_0
        output[1] = y_1 - self.y_0
        self.x_0 = x_1
        self.y_0 = y_1

        return output
