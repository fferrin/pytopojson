from pytopojson import feature, stitch


def planar_ring_area(ring):
    i = 0
    n = len(ring)
    b = ring[n - 1]
    area = 0
    while i < n:
        a, b = b, ring[i]
        area += a[0] * b[1] - a[1] * b[0]
        i += 1
    return abs(area)  # Note: Doubled area!


class MergeArcs(object):
    def __init__(self):
        self.object = feature.Object()
        self.stitch = stitch.Stitch()
        self.polygons_by_arc = dict()
        self.polygons = list()
        self.groups = list()
        self.topology = None

    def __call__(self, topology, objects, *args, **kwargs):
        self.topology = topology

        for o in objects:
            self.geometry(o)

        for polygon in self.polygons:
            if "_" not in polygon:
                group = list()
                polygon["_"] = 1
                neighbors = [polygon]
                polygon = neighbors.pop() if any(neighbors) else False

                while polygon:
                    group.append(polygon)
                    # DictList to list
                    p = list()
                    for i in range(len(polygon) - 1):
                        p.append(polygon[i])
                    for ring in p:
                        for arc in ring:
                            arc = ~arc if arc < 0 else arc
                            for p in self.polygons_by_arc[arc]:
                                if "_" not in p:
                                    p["_"] = 1
                                    neighbors.append(p)

                    polygon = neighbors.pop() if any(neighbors) else False

                for idx, point in enumerate(group):
                    if 1 in point:
                        group[idx] = [point[0], point[1]]
                    else:
                        group[idx] = [point[0]]
                self.groups.append(group)

        for idx, polygon in enumerate(self.polygons):
            if 1 in polygon:
                self.polygons[idx] = [polygon[0], polygon[1]]
            else:
                self.polygons[idx] = [polygon[0]]

        for i, _ in self.polygons_by_arc.items():
            for ii, _ in enumerate(self.polygons_by_arc[i]):
                self.polygons_by_arc[i][ii].pop("_", None)

        return {
            "type": "MultiPolygon",
            "arcs": list(map(lambda x: self._tmp(x), self.groups)),
        }

    def geometry(self, o):
        _type = o["type"]
        if _type == "GeometryCollection":
            for arc in o["geometries"]:
                self.geometry(arc)
        elif _type == "Polygon":
            self.extract(o["arcs"])
        elif _type == "MultiPolygon":
            for arc in o["arcs"]:
                self.extract(arc)

    def extract(self, polygon):
        p = dict()
        for idx, point in enumerate(polygon):
            p[idx] = point

        for ring in polygon:
            for arc in ring:
                arc = ~arc if arc < 0 else arc
                l = self.polygons_by_arc.get(arc, [])
                l.append(p)
                self.polygons_by_arc[arc] = l
        self.polygons.append(p)

    def area(self, ring):
        obj = self.object(self.topology, {"type": "Polygon", "arcs": [ring]})
        return planar_ring_area(obj["coordinates"][0])

    def _tmp(self, polygons):
        arcs = list()
        # Extract the exterior (unique) arcs
        for polygon in polygons:
            for ring in polygon:
                for arc in ring:
                    arc = ~arc if arc < 0 else arc
                    if len(self.polygons_by_arc[arc]) < 2:
                        arcs.append(arc)

        # Stitch the arcs into one or more rings
        arcs = self.stitch(self.topology, arcs)

        # If more than one ring is returned,
        # at most one of these rings can be the exterior;
        # choose the one with the greatest absolute area
        if 1 < len(arcs):
            k = self.area(arcs[0])
            for i in range(1, len(arcs)):
                k_i = self.area(arcs[i])
                if k < k_i:
                    arcs[0], arcs[i] = arcs[i], arcs[0]
                    k = k_i

        return list(filter(lambda x: 0 < len(x), arcs))


class Merge(object):
    def __init__(self):
        self.object = feature.Object()
        self.merge_arcs = MergeArcs()

    def __call__(self, topology, *args, **kwargs):
        arcs = self.merge_arcs(topology, *args)
        return self.object(topology, arcs)
