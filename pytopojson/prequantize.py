class Prequantize(object):
    def __init__(self):
        pass

    def __call__(self, objects, bbox, n, *args, **kwargs):
        self.quantize_geometry_type = {
            "GeometryCollection": self._geometry_collection_call,
            "Point": self._point_call,
            "MultiPoint": self._multi_point_call,
            "LineString": self._line_string_call,
            "MultiLineString": self._multi_line_string_call,
            "Polygon": self._polygon_call,
            "MultiPolygon": self._multi_polygon_call,
        }

        self.x_0, self.y_0, self.x_1, self.y_1 = bbox
        self.k_x = (n - 1) / (self.x_1 - self.x_0) if self.x_0 < self.x_1 else 1
        self.k_y = (n - 1) / (self.y_1 - self.y_0) if self.y_0 < self.y_1 else 1

        for k in objects:
            self.quantize_geometry(objects[k])

        return {
            "scale": [1 / self.k_x, 1 / self.k_y],
            "translate": [self.x_0, self.y_0],
        }

    def _geometry_collection_call(self, o):
        for geom in o["geometries"]:
            self.quantize_geometry(geom)

    def _point_call(self, o):
        o["coordinates"] = self.quantize_point(o["coordinates"])

    def _multi_point_call(self, o):
        o["coordinates"] = list(map(self.quantize_point, o["coordinates"]))

    def _line_string_call(self, o):
        o["arcs"] = self.quantize_line(o["arcs"])

    def _multi_line_string_call(self, o):
        o["arcs"] = list(map(self.quantize_line, o["arcs"]))

    def _polygon_call(self, o):
        o["arcs"] = self.quantize_polygon(o["arcs"])

    def _multi_polygon_call(self, o):
        o["arcs"] = list(map(self.quantize_polygon, o["arcs"]))

    def quantize_point(self, inp):
        return [
            round((inp[0] - self.x_0) * self.k_x),
            round((inp[1] - self.y_0) * self.k_y),
        ]

    def quantize_points(self, inp, m):
        i = j = 0
        n = len(inp)
        output = [None] * n
        p = [None, None]

        while i < n:
            p_i = inp[i]
            x = round((p_i[0] - self.x_0) * self.k_x)
            y = round((p_i[1] - self.y_0) * self.k_y)

            if p != [x, y]:
                p = [x, y]
                output[j] = p
                j += 1

            i += 1

        output = output[:j]

        while j < m:
            output.append([output[0][0], output[0][1]])
            j = len(output)

        return output

    def quantize_line(self, inp):
        return self.quantize_points(inp, 2)

    def quantize_ring(self, inp):
        return self.quantize_points(inp, 4)

    def quantize_polygon(self, inp):
        return list(map(self.quantize_ring, inp))

    def quantize_geometry(self, o):
        if o and o["type"] in self.quantize_geometry_type:
            self.quantize_geometry_type[o["type"]](o)
