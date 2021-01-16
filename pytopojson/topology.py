from pytopojson import (
    bounds,
    cut,
    dedup,
    delta,
    extract,
    geometry,
    prequantize,
)
from pytopojson.hash.hash import HashMap


class Topology(object):
    """
    Constructs the TopoJSON Topology for the specified hash of features.
    Each object in the specified hash must be a GeoJSON object,
    meaning FeatureCollection, a Feature or a geometry object.
    """

    def __init__(self):
        self.bounding_box = bounds.BoundingBox()
        self.cut = cut.Cut()
        self.dedup = dedup.Dedup()
        self.delta = delta.Delta()
        self.extract = extract.Extract()
        self.geometry = geometry.Geometry()
        self.prequantize = prequantize.Prequantize()

    def __call__(self, objects, quantization=-1):
        self.index_geometry_type = {
            "GeometryCollection": self._geometry_collection_call,
            "LineString": self._line_string_call,
            "MultiLineString": self._multi_line_string_call,
            "Polygon": self._polygon_call,
            "MultiPolygon": self._multi_polygon_call,
        }

        objects = self.geometry(objects)
        self.bbox = self.bounding_box(objects)
        self.transform = (
            quantization > 0
            and self.bbox
            and self.prequantize(objects, self.bbox, quantization)
        )
        self.topology = self.dedup(self.cut(self.extract(objects)))
        self.coordinates = self.topology["coordinates"]
        self.index_by_arc = HashMap(
            len(self.topology["arcs"]) * 1.4, self.hash_arc, self.equal_arc
        )

        objects = self.topology["objects"]
        if self.bbox is not None:
            self.topology["bbox"] = self.bbox

        self.topology["arcs"] = list(
            map(
                lambda arc, i: self._slice(arc, i),
                self.topology["arcs"],
                range(len(self.topology["arcs"])),
            )
        )

        self.topology.pop("coordinates", None)
        self.coordinates = None

        for k in objects:
            self.index_geometry(objects[k])

        if self.transform:
            self.topology["transform"] = self.transform
            self.topology["arcs"] = self.delta(self.topology["arcs"])

        return self.topology

    def _slice(self, arc, i):
        self.index_by_arc.set(arc, i)
        return self.coordinates[arc[0] : arc[1] + 1]

    def _geometry_collection_call(self, o):
        list(map(self.index_geometry, o["geometries"]))

    def _line_string_call(self, o):
        o["arcs"] = self.index_arcs(o["arcs"])

    def _multi_line_string_call(self, o):
        o["arcs"] = list(map(self.index_arcs, o["arcs"]))

    def _polygon_call(self, o):
        o["arcs"] = list(map(self.index_arcs, o["arcs"]))

    def _multi_polygon_call(self, o):
        o["arcs"] = list(map(self.index_multi_arcs, o["arcs"]))

    def index_geometry(self, geometry):
        function = self.index_geometry_type.get(geometry["type"], None)
        if geometry and function:
            function(geometry)

    def index_arcs(self, arc):
        indexes = list()

        while arc:
            index = self.index_by_arc.get(arc)
            indexes.append(index if arc[0] < arc[1] else ~index)
            arc = arc.get("next", False)

        return indexes

    def index_multi_arcs(self, arcs):
        return list(map(self.index_arcs, arcs))

    @staticmethod
    def hash_arc(arc):
        i, j = arc[0], arc[1]
        if j < i:
            t = i
            i = j
            j = t

        return i + 31 * j

    @staticmethod
    def equal_arc(arc_a, arc_b):
        i_a, j_a = arc_a[0], arc_a[1]
        i_b, j_b = arc_b[0], arc_b[1]

        if j_a < i_a:
            t = i_a
            i_a = j_a
            j_a = t

        if j_b < i_b:
            t = i_b
            i_b = j_b
            j_b = t

        return i_a == i_b and j_a == j_b
