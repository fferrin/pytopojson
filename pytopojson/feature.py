from pytopojson import transform


class Reverse(object):
    def __init__(self):
        pass

    def __call__(self, array, n, *args, **kwargs):
        j = len(array)
        i = j - n

        j -= 1
        while i < j:
            array[i], array[j] = array[j], array[i]
            i += 1
            j -= 1


class Object(object):
    def __init__(self):
        self.reverse = Reverse()
        self.transform = transform.Transform()
        self.transform_point = None
        self.arcs = None

    def __call__(self, topology, o, *args, **kwargs):
        self.transform_point = self.transform(topology.get("transform", None))
        self.arcs = topology["arcs"]
        return self.geometry(o)

    def arc(self, i, points):
        if any(points):
            points.pop()

        idx = ~i if i < 0 else i
        arcs = self.arcs[idx]
        for k, arc in enumerate(arcs):
            points.append(self.transform_point(arc, k))

        if i < 0:
            self.reverse(points, len(arcs))

    def point(self, p):
        return self.transform_point(p)

    def line(self, arcs):
        points = list()
        for arc in arcs:
            self.arc(arc, points)

        # This should never happen per the specification.
        if len(points) < 2:
            points.append(points[0])

        return points

    def ring(self, arcs):
        points = self.line(arcs)
        # This may happen if an arc has only two points.
        while len(points) < 4:
            points.append(points[0])
        return points

    def polygon(self, arcs):
        return list(map(lambda x: self.ring(x), arcs))

    def geometry(self, o):
        _type = o.get("type", None)

        if _type == "GeometryCollection":
            return {
                "type": _type,
                "geometries": list(map(lambda x: self.geometry(x), o["geometries"])),
            }
        elif _type == "Point":
            coordinates = self.point(o["coordinates"])
        elif _type == "MultiPoint":
            coordinates = list(map(lambda x: self.point(x), o["coordinates"]))
        elif _type == "LineString":
            coordinates = self.line(o["arcs"])
        elif _type == "MultiLineString":
            coordinates = list(map(lambda x: self.line(x), o["arcs"]))
        elif _type == "Polygon":
            coordinates = self.polygon(o["arcs"])
        elif _type == "MultiPolygon":
            coordinates = list(map(lambda x: self.polygon(x), o["arcs"]))
        else:
            return None

        return {"type": _type, "coordinates": coordinates}


class Feature(object):
    def __init__(self):
        self.object = Object()
        self.reverse = Reverse()
        self.transform = transform.Transform()

    def __call__(self, topology, o, *args, **kwargs):
        if isinstance(o, str):
            o = topology["objects"][o]
        if o.get("type", None) == "GeometryCollection":
            return {
                "type": "FeatureCollection",
                "features": list(
                    map(lambda x: self.feature(topology, x), o["geometries"])
                ),
            }
        else:
            return self.feature(topology, o)

    def feature(self, topology, o):
        feat = {
            "id": o.get("id", None),
            "bbox": o.get("bbox", None),
            "type": "Feature",
            "properties": o.get("properties", dict()),
            "geometry": self.object(topology, o),
        }

        for k in ("id", "bbox"):
            if feat[k] is None:
                del feat[k]

        return feat
