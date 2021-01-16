from pytopojson import commons, feature, stitch


class ExtractArcs(object):
    def __init__(self):
        self.arcs = list()
        self.geoms_by_arc = list()
        self.geom = None

    def __call__(self, topology, object, filter, *args, **kwargs):
        self.geometry(object)

        for geoms in self.geoms_by_arc:
            if filter is None:
                self.arcs.append(geoms[0]["i"])
            else:
                if filter(geoms[0]["g"], geoms[-1]["g"]):
                    self.arcs.append(geoms[0]["i"])

        return self.arcs

    def extract_0(self, i):
        j = ~i if i < 0 else i
        self.geoms_by_arc.get(j, []).append({"i": i, "g": self.geom})

    def extract_1(self, arcs):
        for arc in arcs:
            self.extract_0(arc)

    def extract_2(self, arcs):
        for arc in arcs:
            self.extract_1(arc)

    def extract_3(self, arcs):
        for arc in arcs:
            self.extract_2(arc)

    def geometry(self, o):
        self.geom = o
        _type = o["type"]
        if _type == "GeometryCollection":
            for g in o["geometries"]:
                self.geometry(g)
        elif _type == "LineString":
            self.extract_1(o["arcs"])
        elif _type == "MultiLineString" or _type == "Polygon":
            self.extract_2(o["arcs"])
        elif _type == "MultiPolygon":
            self.extract_3(o["arcs"])


class MeshArcs(object):
    def __init__(self):
        self.stitch = stitch.Stitch()
        self.extract_arcs = ExtractArcs()

    def __call__(self, topology, obj=None, filt=None, *args, **kwargs):
        if obj is not None and filt is not None:
            arcs = self.extract_arcs(topology, obj, filt)
        else:
            n = len(topology["arcs"])
            arcs = [i for i in range(n)]
        return {"type": "MultiLineString", "arcs": self.stitch(topology, arcs)}


class Mesh(object):
    def __init__(self):
        self.object = feature.Object()
        self.mesh_arcs = MeshArcs()

    def __call__(self, topology, *args, **kwargs):
        arcs = self.mesh_arcs(topology, *args)
        return self.object(topology, arcs)
