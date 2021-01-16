class Extract(object):
    """
    Extracts the lines and rings from the specified hash of geometry objects.

    Returns an object with three properties:

    * coordinates - shared buffer of [x, y] coordinates
    * lines - lines extracted from the hash, of the form [start, end]
    * rings - rings extracted from the hash, of the form [start, end]

    For each ring or line, start and end represent inclusive indexes into the
    coordinates buffer. For rings (and closed lines), coordinates[start] equals
    coordinates[end].

    For each line or polygon geometry in the input hash, including nested
    geometries as in geometry collections, the `coordinates` array is replaced
    with an equivalent `arcs` array that, for each line (for line string
    geometries) or ring (for polygon geometries), points to one of the above
    lines or rings.
    """

    def __init__(self):
        pass

    def __call__(self, objects, *args, **kwargs):
        self.extract_geometry_type = {
            "GeometryCollection": self._geometry_collection_call,
            "LineString": self._line_string_call,
            "MultiLineString": self._multi_line_string_call,
            "Polygon": self._polygon_call,
            "MultiPolygon": self._multi_polygon_call,
        }

        self.index = 0
        self.lines = list()
        self.rings = list()
        self.coordinates = list()

        for k in objects:
            self.extract_geometry(objects[k])

        return {
            "type": "Topology",
            "coordinates": self.coordinates,
            "lines": self.lines,
            "rings": self.rings,
            "objects": objects,
        }

    def _line_string_call(self, o):
        o["arcs"] = self.extract_line(o["arcs"])

    def _multi_line_string_call(self, o):
        o["arcs"] = list(map(self.extract_line, o["arcs"]))

    def _polygon_call(self, o):
        o["arcs"] = list(map(self.extract_ring, o["arcs"]))

    def _multi_polygon_call(self, o):
        o["arcs"] = list(map(self.extract_multi_ring, o["arcs"]))

    def _geometry_collection_call(self, o):
        for geometry in o["geometries"]:
            self.extract_geometry(geometry)

    def extract_geometry(self, geometry):
        if geometry and geometry["type"] in self.extract_geometry_type:
            self.extract_geometry_type[geometry["type"]](geometry)

    def extract(self, geometry, append_to):
        i = 0
        n = len(geometry)

        while i < n:
            self.coordinates.append(geometry[i])
            self.index += 1
            i += 1

        arc = [self.index - n, self.index - 1]

        append_to.append(arc)

        return arc

    def extract_line(self, line):
        return self.extract(line, self.lines)

    def extract_ring(self, ring):
        return self.extract(ring, self.rings)

    def extract_multi_ring(self, rings):
        return list(map(self.extract_ring, rings))
