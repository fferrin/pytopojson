# Computes the bounding box of the specified hash of GeoJSON objects.
class BoundingBox(object):
    def __init__(self):
        self.x_0 = self.y_0 = float("inf")
        self.x_1 = self.y_1 = -float("inf")

    def __call__(self, geometry, *args, **kwargs):
        self.bound_geometry_type = {
            "GeometryCollection": lambda o: list(
                map(self.bound_geometry, o["geometries"])
            ),
            "Point": lambda o: self.bound_point(o["coordinates"]),
            "MultiPoint": lambda o: list(map(self.bound_point, o["coordinates"])),
            "LineString": lambda o: self.bound_line(o["arcs"]),
            "MultiLineString": lambda o: list(map(self.bound_line, o["arcs"])),
            "Polygon": lambda o: list(map(self.bound_line, o["arcs"])),
            "MultiPolygon": lambda o: list(map(self.bound_multiline, o["arcs"])),
        }

        for k in geometry:
            self.bound_geometry(geometry[k])

        self.value = (
            [self.x_0, self.y_0, self.x_1, self.y_1]
            if self.x_0 <= self.x_1 and self.y_0 <= self.y_1
            else None
        )
        return self.value

    def bound_geometry(self, geometry):
        if geometry and geometry["type"] in self.bound_geometry_type:
            self.bound_geometry_type[geometry["type"]](geometry)

    def bound_point(self, coordinates):
        x, y = coordinates
        self.x_0 = min(x, self.x_0)
        self.y_0 = min(y, self.y_0)
        self.x_1 = max(x, self.x_1)
        self.y_1 = max(y, self.y_1)

    def bound_line(self, coordinates):
        list(map(self.bound_point, coordinates))

    def bound_multiline(self, coordinates):
        list(map(self.bound_line, coordinates))
