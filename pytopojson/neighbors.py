from pytopojson import bisect


class Neighbors(object):
    def __init__(self):
        self.bisect = bisect.Bisect()
        self.indexes_by_arc = None
        self.neighbors = None
        self.geometry_type = {
            "LineString": self.line,
            "MultiLineString": self.polygon,
            "Polygon": self.polygon,
            "MultiPolygon": self.multipolygon,
        }

    def __call__(self, objects, *args, **kwargs):
        self.indexes_by_arc = dict()  # Arc index -> array of object indexes
        self.neighbors = [[] for _ in objects]

        for idx, o in enumerate(objects):
            self.geometry(o, idx)

        for i in self.indexes_by_arc:
            indexes = self.indexes_by_arc[i]
            for j in range(len(indexes)):
                for k in range(j + 1, len(indexes)):
                    ij = indexes[j]
                    ik = indexes[k]

                    n = self.neighbors[ij]
                    i = self.bisect(n, ik)
                    if i >= len(n) or n[i] != ik:
                        self.neighbors[ij] = n[:i] + [ik] + n[i:]

                    n = self.neighbors[ik]
                    i = self.bisect(n, ij)
                    if i >= len(n) or n[i] != ij:
                        self.neighbors[ik] = n[:i] + [ij] + n[i:]

        return self.neighbors

    def line(self, arcs, i):
        for a in arcs:
            if a < 0:
                a = ~a

            if a in self.indexes_by_arc:
                self.indexes_by_arc[a].append(i)
            else:
                self.indexes_by_arc[a] = [i]

    def polygon(self, arcs, i):
        for arc in arcs:
            self.line(arc, i)

    def multipolygon(self, arcs, i):
        for arc in arcs:
            self.polygon(arc, i)

    def geometry(self, o, i):
        if o["type"] == "GeometryCollection":
            for geom in o["geometries"]:
                self.geometry(geom, i)
        elif o["type"] in self.geometry_type.keys():
            self.geometry_type[o["type"]](o["arcs"], i)
