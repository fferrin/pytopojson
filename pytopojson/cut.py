from pytopojson.join import Join


class Cut(object):
    """
    Given an extracted (pre-)topology, cuts (or rotates) arcs so that all shared
    point sequences are identified. The topology can then be subsequently deduped
    to remove exact duplicate arcs.
    """

    def __init__(self):
        self.join = Join()

    def __call__(self, topology, *args, **kwargs):
        self.junctions = self.join(topology)
        self.coordinates = topology["coordinates"]
        self.lines = list()
        self.rings = list()
        self.index = 0
        self.cut_geometry_type = {
            "GeometryCollection": self._geometry_collection_call,
            "LineString": self._line_string_call,
            "MultiLineString": self._multi_line_string_call,
            "Polygon": self._polygon_call,
            "MultiPolygon": self._multi_polygon_call,
        }

        for k, v in topology["objects"].items():
            self.cut_geometry(v)

        topology["lines"] = self.lines
        topology["rings"] = self.rings
        return topology

    def rotate_array(self, array, start, end, offset):
        self.reverse(array, start, end)
        self.reverse(array, start, start + offset)
        self.reverse(array, start + offset, end)

    def reverse(self, array, start, end):
        mid = start + ((end - start) >> 1)
        end -= 1

        while start < mid:
            t = array[start]
            array[start] = array[end]
            array[end] = t

            start += 1
            end -= 1

    def _line_string_call(self, o):
        o["arcs"] = self.cut_line(o["arcs"])

    def _multi_line_string_call(self, o):
        o["arcs"] = list(map(self.cut_line, o["arcs"]))

    def _polygon_call(self, o):
        o["arcs"] = list(map(self.cut_ring, o["arcs"]))

    def _multi_polygon_call(self, o):
        o["arcs"] = list(map(self.cut_multi_ring, o["arcs"]))

    def _geometry_collection_call(self, o):
        for geometry in o["geometries"]:
            self.cut_geometry(geometry)

    def cut_line(self, line):
        line = dict({0: line[0], 1: line[1]})
        line_mid = line[0] + 1
        line_end = line[1]

        l = line
        while line_mid < line_end:
            if self.junctions.has(self.coordinates[line_mid]):
                next = {0: line_mid, 1: l[1]}
                l[1] = line_mid
                l["next"] = next
                l = next

            line_mid += 1

        self.lines.append(line)
        return line

    def cut_ring(self, ring):
        ring = dict({0: ring[0], 1: ring[1]})
        ring_start = ring[0]
        ring_mid = ring_start
        ring_end = ring[1]
        ring_fixed = self.junctions.has(self.coordinates[ring_mid])

        ring_mid += 1
        r = ring
        while ring_mid < ring_end:
            if self.junctions.has(self.coordinates[ring_mid]):
                if ring_fixed:
                    next = {0: ring_mid, 1: r[1]}
                    r[1] = ring_mid
                    r["next"] = next
                    r = next
                # For the first junction, we can rotate rather than cut.
                else:
                    self.rotate_array(
                        self.coordinates, ring_start, ring_end, ring_end - ring_mid
                    )
                    self.coordinates[ring_end] = self.coordinates[ring_start]
                    ring_fixed = True
                    ring_mid = ring_start

            ring_mid += 1

        self.rings.append(ring)
        return ring

    def cut_multi_ring(self, rings):
        return list(map(self.cut_ring, rings))

    def cut_geometry(self, geometry):
        if geometry and geometry["type"] in self.cut_geometry_type:
            self.cut_geometry_type[geometry["type"]](geometry)
