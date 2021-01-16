import math

from pytopojson import transform


class BBox(object):
    def __init__(self):
        self.transform = transform.Transform()
        self.x_0 = math.inf
        self.y_0 = self.x_0
        self.x_1 = -self.x_0
        self.y_1 = -self.x_0
        self.t = None

    def __call__(self, topology, *args, **kwargs):
        self.t = self.transform(topology.get("transform", None))

        for arc in topology["arcs"]:
            i = 0
            n = len(arc)

            while i < n:
                p = self.t(arc[i], i)
                if p[0] < self.x_0:
                    self.x_0 = p[0]
                if self.x_1 < p[0]:
                    self.x_1 = p[0]
                if p[1] < self.y_0:
                    self.y_0 = p[1]
                if self.y_1 < p[1]:
                    self.y_1 = p[1]
                i += 1

        for k in topology["objects"]:
            self.bbox_geometry(topology["objects"][k])

        return [self.x_0, self.y_0, self.x_1, self.y_1]

    def bbox_point(self, p):
        p = self.t(p)
        if p[0] < self.x_0:
            self.x_0 = p[0]
        if self.x_1 < p[0]:
            self.x_1 = p[0]
        if p[1] < self.y_0:
            self.y_0 = p[1]
        if self.y_1 < p[1]:
            self.y_1 = p[1]

    def bbox_geometry(self, o):
        if o["type"] == "GeometryCollection":
            for geom in o["geometries"]:
                self.bbox_geometry(geom)
        elif o["type"] == "Point":
            self.bbox_point(o["coordinates"])
        elif o["type"] == "MultiPoint":
            for coord in o["coordinates"]:
                self.bbox_point(coord)
