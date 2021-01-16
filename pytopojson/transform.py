from pytopojson import identity


class Transform(object):
    def __init__(self):
        self.identity = identity.Identity()
        self.x_0, self.y_0 = 0, 0
        self.k_x, self.k_y = 0, 0
        self.d_x, self.d_y = 0, 0

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

        self.x_0 += input[0]
        self.y_0 += input[1]
        output[0] = self.x_0 * self.k_x + self.d_x
        output[1] = self.y_0 * self.k_y + self.d_y

        return output
