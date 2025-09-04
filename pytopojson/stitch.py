from functools import reduce
from operator import iadd, itemgetter

class Fragment:
    def __init__(self, start, end, data):
        self.start = start
        self.end = end
        self.data = data

    def append(self, item):
        self.data.append(item)

    def unshift(self, value):
        self.data.insert(0, value)

    def __eq__(self, o):
        if isinstance(o, Fragment):
            return (
                self.data == o.data and
                self.start == o.start and
                self.end == o.end
            )
        return False

    def __add__(self, o):
        return Fragment(None, None, self.data + o.data)

    def __str__(self):
        return f"[{self.data}, start: {self.start}, end: {self.end}]"

class Stitch(object):
    def __init__(self):
        pass

    def __call__(self, topology, arcs, *args, **kwargs):
        self.stitched_arcs = {}
        self.fragment_by_start = {}
        self.fragment_by_end = {}
        self.fragments = []
        self.empty_index = -1
        self.topology = topology

        # Stitch empty arcs first, since they may be subsumed by other arcs.
        # j: index used for the `arcs` list
        # i: index used for the `topology["arcs"]` list
        for j, i in enumerate(arcs):
            arc = self.topology["arcs"][~i if i < 0 else i]
            if len(arc) < 3 and not arc[1][0] and not arc[1][1]:
                self.empty_index += 1
                t = arcs[self.empty_index]
                arcs[self.empty_index] = i
                arcs[j] = t

        # q, r = divmod(len(arcs), 10)
        # print("[")
        # for i in range(q):
        #     values = arcs[10 * i: 10 * (i + 1)]
        #     print(",".join(map(lambda x: f"{x:>6}", values)))
        # values = arcs[10 * (i + 1): 10 * (i + 1) + r]
        # print(",".join(map(lambda x: f"{x:>6}", values)))
        # print("]")
        # print(len(arcs))

        for i in arcs:
            start, end = self.ends(i)
            if start in self.fragment_by_end:
                f = self.fragment_by_end[start]
                self.fragment_by_end.pop(f.end, None)
                f.append(i)
                f.end = end
                if end in self.fragment_by_start:
                    g = self.fragment_by_start[end]
                    self.fragment_by_start.pop(g.start, None)
                    fg = f if g == f else f + g
                    fg.start = f.start
                    fg.end = g.end
                    self.fragment_by_start[fg.start] = fg
                    self.fragment_by_end[fg.end] = fg
                else:
                    self.fragment_by_start[f.start] = f
                    self.fragment_by_end[f.end] = f
            elif end in self.fragment_by_start:
                f = self.fragment_by_start[end]
                self.fragment_by_start.pop(f.start, None)
                f.unshift(i)
                f.start = start
                if start in self.fragment_by_end:
                    g = self.fragment_by_end[start]
                    self.fragment_by_end.pop(g.end, None)
                    gf = f if g == f else g + f
                    gf.start = g.start
                    gf.end = f.end
                    self.fragment_by_start[gf.start] = gf
                    self.fragment_by_end[gf.end] = gf
                else:
                    self.fragment_by_start[f.start] = f
                    self.fragment_by_end[f.end] = f
            else:
                f = Fragment(start, end, [i])
                self.fragment_by_start[f.start] = f
                self.fragment_by_end[f.end] = f

        self.flush(self.fragment_by_end, self.fragment_by_start)
        self.flush(self.fragment_by_start, self.fragment_by_end)

        for i in arcs:
            if not self.stitched_arcs.get(~i if i < 0 else i):
                self.fragments.append([i])

        return self.fragments

    def ends(self, i):
        arc = self.topology["arcs"][~i if i < 0 else i]
        p0 = arc[0]

        if "transform" in self.topology:
            p1 = [
                reduce(iadd, map(itemgetter(0), arc)),
                reduce(iadd, map(itemgetter(1), arc)),
            ]
        else:
            p1 = arc[-1]

        p0 = tuple(p0)
        p1 = tuple(p1)
        return (p1, p0) if i < 0 else (p0, p1)

    def flush(self, fragment_by_end, fragment_by_start):
        for f in fragment_by_end.values():
            fragment_by_start.pop(f.start, None)
            f = f.data
            for i in f:
                self.stitched_arcs[~i if i < 0 else i] = 1
            self.fragments.append(f)
