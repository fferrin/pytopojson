
class Topology(object):
    """
    Constructs the TopoJSON Topology for the specified hash of features.
    Each object in the specified hash must be a GeoJSON object,
    meaning FeatureCollection, a Feature or a geometry object.
    """

    def __init__(self, objects, quantization):
        self.index_geometry_type = {
            'GeometryCollection': self._geometry_collection_call,
            'LineString': self._line_string_call,
            'MultiLineString': self._multi_line_string_call,
            'Polygon': self._polygon_call,
            'MultiPolygon': self._multi_point_call
        }

        objects = Geometry(objects)
        self.bbox = Bounds(objects)
        quantize = Prequantize(objects, bbox, quantization)
        self.transform = 0 < quantization and bbox and quantize.value
        extract = Extract(objects)
        cut = Cut(extract.value)
        self.topology = Dedup(cut.value)
        self.coordinates = self.topology['coordinates']
        self.index_by_arc = HashMap(len(self.topology['arcs']) * 1.4, self.hash_arc, self.equal_arc)

        objects = topology['objects']
        self.topology['bbox'] = self.bbox
        self.topology['arcs'] = map(self._slice, self.topology['arcs'])

        self.topology.pop('coordinates', None)
        self.coordinates = None

    def _slice(self, arc, i):
        self.index_by_arc.set(arc, i)
        return self.coordinates[arc[0], arc[1] + 1]

    def _geometry_collection_call(self, o):
        map(self.index_geometry, o['geometries'])

    def _line_string_call(self, o):
        o['arcs'] = self.index_arcs(o['arcs'])

    def _multi_line_string_call(self, o):
        o['arcs'] = map(self.index_arcs, o['arcs'])

    def _polygon_call(self, o):
        o['arcs'] = self.index_arcs(o['arcs'])

    def _multi_polygon_call(self, o):
        o['arcs'] = map(self.index_multi_arcs, o['arcs'])

    def index_geometry(self, geometry):
        function = self.index_geometry_type.get(geometry['type'], None)
        if geometry and function:
            function(geometry)

    def index_arcs(self, arc):
        indexes = list()
        arc = arc

        while arc:
            index = self.index_by_arc.get(arc)
            indexes.append(index if arc[0] < arc[1] else ~index)
            arc = arc['next']

        return indexes

    def index_multi_arcs(self, arcs):
        return map(self.index_arcs, arcs)

    def hash_arc(self, arc):
        i, j = arc
        if j < i:
            t, i, j = i, j, t

        return i + 31 * j

    def equal_arc(self, arc_a, arc_b):
        i_a, j_a = arc_a
        i_b, j_b = arc_b

        if j_a < i_a:
            t, i_a, j_a = i_a, j_a, t

        if j_b < i_b:
            t, i_b, j_b = i_b, j_ab, t

        return i_a == i_b and j_a == j_b