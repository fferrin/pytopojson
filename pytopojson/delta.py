class Delta(object):
    def __init__(self):
        pass

    def __call__(self, arcs, *args, **kwargs):
        i = 0
        n = len(arcs)

        while i < n:
            arc = arcs[i]
            j = k = 1
            m = len(arc)
            point = arc[0]
            x_0, y_0 = point

            while j < m:
                point = arc[j]
                x_1, y_1 = point
                if x_0 != x_1 or y_0 != y_1:
                    arc[k] = [x_1 - x_0, y_1 - y_0]
                    x_0 = x_1
                    y_0 = y_1
                    k += 1

                j += 1

            # Each arc must be an array of two or more positions.
            if k == 1:
                arc[k] = [0, 0]
                k += 1

            arcs[i] = arc[:k]
            i += 1

        return arcs
