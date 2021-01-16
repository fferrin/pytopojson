import unittest

from pytopojson import geometry


class GeometryTestCase(unittest.TestCase):
    def setUp(self):
        self.geometry = geometry.Geometry()

    def test_geometry_replaces_LineString_Feature_with_LineString_Geometry(self):
        geom = self.geometry(
            {
                "foo": {
                    "type": "Feature",
                    "geometry": {"type": "LineString", "coordinates": [[0, 0]]},
                }
            }
        )

        self.assertDictEqual(geom, {"foo": {"type": "LineString", "arcs": [[0, 0]]}})

    def test_geometry_replaces_GeometryCollection_Feature_with_GeometryCollection(self):
        geom = self.geometry(
            {
                "foo": {
                    "type": "Feature",
                    "geometry": {
                        "type": "GeometryCollection",
                        "geometries": [{"type": "LineString", "coordinates": [[0, 0]]}],
                    },
                }
            }
        )

        self.assertDictEqual(
            geom,
            {
                "foo": {
                    "type": "GeometryCollection",
                    "geometries": [{"type": "LineString", "arcs": [[0, 0]]}],
                }
            },
        )

    def test_geometry_replaces_FeatureCollection_with_GeometryCollection(self):
        geom = self.geometry(
            {
                "foo": {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "geometry": {"type": "LineString", "coordinates": [[0, 0]]},
                        }
                    ],
                }
            }
        )

        self.assertDictEqual(
            geom,
            {
                "foo": {
                    "type": "GeometryCollection",
                    "geometries": [{"type": "LineString", "arcs": [[0, 0]]}],
                }
            },
        )

    def test_geometry_replaces_Feature_with_null_Geometry_with_null_type_Geometry(self):
        geom = self.geometry({"foo": {"type": "Feature", "geometry": None}})

        self.assertDictEqual(geom, {"foo": {"type": None}})

    def test_geometry_replaces_top_level_null_Geometry_with_null_type_Geometry(self):
        geom = self.geometry({"foo": None})

        self.assertDictEqual(geom, {"foo": {"type": None}})

    def test_geometry_replaces_null_Geometry_in_GeometryCollection_with_null_type_Geometry(
        self,
    ):
        geom = self.geometry(
            {"foo": {"type": "GeometryCollection", "geometries": [None]}}
        )

        self.assertDictEqual(
            geom,
            {"foo": {"type": "GeometryCollection", "geometries": [{"type": None}]}},
        )

    def test_geometry_preserves_id(self):
        geom = self.geometry(
            {
                "foo": {
                    "id": "foo",
                    "type": "Feature",
                    "geometry": {"type": "LineString", "coordinates": [[0, 0]]},
                }
            }
        )

        self.assertDictEqual(
            geom, {"foo": {"id": "foo", "type": "LineString", "arcs": [[0, 0]]}}
        )

    def test_geometry_preserves_properties_if_non_empty(self):
        geom = self.geometry(
            {
                "foo": {
                    "properties": {"foo": 42},
                    "type": "Feature",
                    "geometry": {"type": "LineString", "coordinates": [[0, 0]]},
                }
            }
        )

        self.assertDictEqual(
            geom,
            {
                "foo": {
                    "properties": {"foo": 42},
                    "type": "LineString",
                    "arcs": [[0, 0]],
                }
            },
        )

    def test_geometry_applies_a_shallow_copy_for_properties(self):
        input = {
            "foo": {
                "properties": {"foo": 42},
                "type": "Feature",
                "geometry": {"type": "LineString", "coordinates": [[0, 0]]},
            }
        }

        geom = self.geometry(input)

        self.assertDictEqual(input["foo"]["properties"], geom["foo"]["properties"])

    def test_geometry_deletes_empty_properties(self):
        geom = self.geometry(
            {
                "foo": {
                    "properties": {},
                    "type": "Feature",
                    "geometry": {"type": "LineString", "coordinates": [[0, 0]]},
                }
            }
        )

        self.assertDictEqual(geom, {"foo": {"type": "LineString", "arcs": [[0, 0]]}})

    def test_geometry_does_not_convert_singular_multipoints_to_points(self):
        geom = self.geometry({"foo": {"type": "MultiPoint", "coordinates": [[0, 0]]}})

        self.assertDictEqual(
            geom, {"foo": {"type": "MultiPoint", "coordinates": [[0, 0]]}}
        )

    def test_geometry_does_not_convert_empty_multipoints_to_null(self):
        geom = self.geometry({"foo": {"type": "MultiPoint", "coordinates": []}})

        self.assertDictEqual(geom, {"foo": {"type": "MultiPoint", "coordinates": []}})

    def test_geometry_does_not_convert_singular_multilines_to_lines(self):
        geom = self.geometry(
            {"foo": {"type": "MultiLineString", "coordinates": [[[0, 0], [0, 1]]]}}
        )

        self.assertDictEqual(
            geom, {"foo": {"type": "MultiLineString", "arcs": [[[0, 0], [0, 1]]]}}
        )

    def test_geometry_does_not_convert_empty_lines_to_null(self):
        geom = self.geometry({"foo": {"type": "LineString", "coordinates": []}})

        self.assertDictEqual(geom, {"foo": {"type": "LineString", "arcs": []}})

    def test_geometry_does_not_convert_empty_multilines_to_null(self):
        geom = self.geometry(
            {
                "foo": {"type": "MultiLineString", "coordinates": []},
                "bar": {"type": "MultiLineString", "coordinates": [[]]},
            }
        )

        self.assertDictEqual(
            geom,
            {
                "foo": {"type": "MultiLineString", "arcs": []},
                "bar": {"type": "MultiLineString", "arcs": [[]]},
            },
        )

    def test_geometry_does_not_strip_empty_rings_in_polygons(self):
        geom = self.geometry(
            {
                "foo": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 0]], []],
                }
            }
        )

        self.assertDictEqual(
            geom,
            {
                "foo": {
                    "type": "Polygon",
                    "arcs": [[[0, 0], [1, 0], [1, 1], [0, 0]], []],
                }
            },
        )

    def test_geometry_does_not_strip_empty_lines_in_multilines(self):
        geom = self.geometry(
            {
                "foo": {
                    "type": "MultiLineString",
                    "coordinates": [
                        [[0, 0], [1, 0], [1, 1], [0, 0]],
                        [],
                        [[0, 0], [1, 0]],
                    ],
                }
            }
        )

        self.assertDictEqual(
            geom,
            {
                "foo": {
                    "type": "MultiLineString",
                    "arcs": [[[0, 0], [1, 0], [1, 1], [0, 0]], [], [[0, 0], [1, 0]]],
                }
            },
        )

    def test_geometry_does_not_convert_empty_polygons_to_null(self):
        geom = self.geometry(
            {
                "foo": {"type": "Polygon", "coordinates": []},
                "bar": {"type": "Polygon", "coordinates": [[]]},
            }
        )

        self.assertDictEqual(
            geom,
            {
                "foo": {"type": "Polygon", "arcs": []},
                "bar": {"type": "Polygon", "arcs": [[]]},
            },
        )

    def test_geometry_does_not_strip_empty_polygons_in_multipolygons(self):
        geom = self.geometry(
            {
                "foo": {
                    "type": "MultiPolygon",
                    "coordinates": [[[[0, 0], [1, 0], [1, 1], [0, 0]], []], [], [[]]],
                }
            }
        )

        self.assertDictEqual(
            geom,
            {
                "foo": {
                    "type": "MultiPolygon",
                    "arcs": [[[[0, 0], [1, 0], [1, 1], [0, 0]], []], [], [[]]],
                }
            },
        )

    def test_geometry_does_not_convert_singular_multipolygons_to_polygons(self):
        geom = self.geometry(
            {
                "foo": {
                    "type": "MultiPolygon",
                    "coordinates": [[[[0, 0], [0, 1], [1, 0], [0, 0]]]],
                }
            }
        )

        self.assertDictEqual(
            geom,
            {
                "foo": {
                    "type": "MultiPolygon",
                    "arcs": [[[[0, 0], [0, 1], [1, 0], [0, 0]]]],
                }
            },
        )
