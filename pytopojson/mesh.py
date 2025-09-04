from pytopojson import feature, stitch


class ExtractArcs(object):
    def __init__(self):
        self.geoms_by_arc = {}
        self.geom = None

    def __call__(self, topology, obj, filt, *args, **kwargs):
        arcs = []
        self.geometry(obj)

        list_geoms = [self.geoms_by_arc[key] for key in sorted(self.geoms_by_arc)]
        if filt is None:
            for geoms in list_geoms:
                arcs.append(geoms[0]["i"])
        else:
            for geoms in list_geoms:
                if filt(geoms[0]["g"], geoms[-1]["g"]):
                    arcs.append(geoms[0]["i"])

        return arcs

    def extract_0(self, i):
        j = ~i if i < 0 else i
        self.geoms_by_arc.setdefault(j, []).append({"i": i, "g": self.geom})

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
        if obj is None:
            arcs = list(range(len(topology["arcs"])))
        else:
            arcs = self.extract_arcs(topology, obj, filt)
            # q, r = divmod(len(arcs), 10)
            # print("[")
            # for i in range(q):
            #     values = arcs[10 * i: 10 * (i + 1)]
            #     print(",".join(map(lambda x: f"{x:>6}", values)))
            # print("]")
        return {"type": "MultiLineString", "arcs": self.stitch(topology, arcs)}


class Mesh(object):
    def __init__(self):
        self.object = feature.Object()
        self.mesh_arcs = MeshArcs()

    def __call__(self, topology, *args, **kwargs):
        arcs = self.mesh_arcs(topology, *args, **kwargs)
        return self.object(topology, arcs, *args, **kwargs)
