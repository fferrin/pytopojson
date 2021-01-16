import json
import math
import unittest

from pytopojson import feature


class FeatureTestCase(unittest.TestCase):
    def setUp(self):
        self.feature = feature.Feature()

    @staticmethod
    def _load_json_file(filepath):
        with open(filepath, "r") as src:
            return json.load(src)

    @staticmethod
    def simple_topology(obj):
        return {
            "type": "Topology",
            "transform": {"scale": [1, 1], "translate": [0, 0]},
            "objects": {"foo": obj},
            "arcs": [
                [[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1]],
                [[0, 0], [1, 0], [0, 1]],
                [[1, 1], [-1, 0], [0, -1]],
                [[1, 1]],
                [[0, 0]],
            ],
        }

    def test_feature_the_geometry_type_is_preserved(self):
        t = self.simple_topology({"type": "Polygon", "arcs": [[0]]})
        self.assertEqual(
            self.feature(t, t["objects"]["foo"])["geometry"]["type"], "Polygon"
        )

    def test_feature_point_is_a_valid_geometry_type(self):
        t = self.simple_topology({"type": "Point", "coordinates": [0, 0]})
        self.assertDictEqual(
            {
                "type": "Feature",
                "properties": {},
                "geometry": {"type": "Point", "coordinates": [0, 0]},
            },
            self.feature(t, t["objects"]["foo"]),
        )

    def test_feature_MultiPoint_is_a_valid_geometry_type(self):
        t = self.simple_topology({"type": "MultiPoint", "coordinates": [[0, 0]]})
        self.assertDictEqual(
            {
                "type": "Feature",
                "properties": {},
                "geometry": {"type": "MultiPoint", "coordinates": [[0, 0]]},
            },
            self.feature(t, t["objects"]["foo"]),
        )

    def test_feature_LineString_is_a_valid_geometry_type(self):
        t = self.simple_topology({"type": "LineString", "arcs": [0]})
        self.assertDictEqual(
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]],
                },
            },
            self.feature(t, t["objects"]["foo"]),
        )

    def test_feature_MultiLineString_is_a_valid_geometry_type(self):
        t = self.simple_topology({"type": "MultiLineString", "arcs": [[0]]})
        self.assertDictEqual(
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "MultiLineString",
                    "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]],
                },
            },
            self.feature(t, t["objects"]["foo"]),
        )

    def test_feature_line_strings_have_at_least_two_coordinates(self):
        t = self.simple_topology({"type": "LineString", "arcs": [3]})
        self.assertDictEqual(
            {
                "type": "Feature",
                "properties": {},
                "geometry": {"type": "LineString", "coordinates": [[1, 1], [1, 1]]},
            },
            self.feature(t, t["objects"]["foo"]),
        )

        t = self.simple_topology({"type": "MultiLineString", "arcs": [[3], [4]]})
        self.assertDictEqual(
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "MultiLineString",
                    "coordinates": [[[1, 1], [1, 1]], [[0, 0], [0, 0]]],
                },
            },
            self.feature(t, t["objects"]["foo"]),
        )

    def test_feature_Polygon_is_a_valid_feature_type(self):
        t = self.simple_topology({"type": "Polygon", "arcs": [[0]]})
        self.assertDictEqual(
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]],
                },
            },
            self.feature(t, t["objects"]["foo"]),
        )

    def test_feature_MultiPolygon_is_a_valid_feature_type(self):
        t = self.simple_topology({"type": "MultiPolygon", "arcs": [[[0]]]})
        self.assertDictEqual(
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": [[[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]],
                },
            },
            self.feature(t, t["objects"]["foo"]),
        )

    def test_feature_polygons_are_closed_with_at_least_four_coordinates(self):
        topology = {
            "type": "Topology",
            "transform": {"scale": [1, 1], "translate": [0, 0]},
            "objects": {
                "foo": {"type": "Polygon", "arcs": [[0]]},
                "bar": {"type": "Polygon", "arcs": [[0, 1]]},
            },
            "arcs": [[[0, 0], [1, 1]], [[1, 1], [-1, -1]]],
        }
        self.assertListEqual(
            self.feature(topology, topology["objects"]["foo"])["geometry"][
                "coordinates"
            ],
            [[[0, 0], [1, 1], [0, 0], [0, 0]]],
        )
        self.assertListEqual(
            self.feature(topology, topology["objects"]["bar"])["geometry"][
                "coordinates"
            ],
            [[[0, 0], [1, 1], [0, 0], [0, 0]]],
        )

    def test_feature_top_level_geometry_collections_are_mapped_to_feature_collections(
        self,
    ):
        t = self.simple_topology(
            {
                "type": "GeometryCollection",
                "geometries": [{"type": "MultiPolygon", "arcs": [[[0]]]}],
            }
        )
        self.assertDictEqual(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {},
                        "geometry": {
                            "type": "MultiPolygon",
                            "coordinates": [[[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]],
                        },
                    }
                ],
            },
            self.feature(t, t["objects"]["foo"]),
        )

    def test_feature_geometry_collections_can_be_nested(self):
        t = self.simple_topology(
            {
                "type": "GeometryCollection",
                "geometries": [
                    {
                        "type": "GeometryCollection",
                        "geometries": [{"type": "Point", "coordinates": [0, 0]}],
                    }
                ],
            }
        )
        self.assertDictEqual(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {},
                        "geometry": {
                            "type": "GeometryCollection",
                            "geometries": [{"type": "Point", "coordinates": [0, 0]}],
                        },
                    }
                ],
            },
            self.feature(t, t["objects"]["foo"]),
        )

    def test_feature_top_level_geometry_collections_do_not_have_ids_but_second_level_geometry_collections_can(
        self,
    ):
        t = self.simple_topology(
            {
                "type": "GeometryCollection",
                "id": "collection",
                "geometries": [
                    {
                        "type": "GeometryCollection",
                        "id": "feature",
                        "geometries": [
                            {"type": "Point", "id": "geometry", "coordinates": [0, 0]}
                        ],
                    }
                ],
            }
        )
        self.assertDictEqual(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "id": "feature",
                        "properties": {},
                        "geometry": {
                            "type": "GeometryCollection",
                            "geometries": [{"type": "Point", "coordinates": [0, 0]}],
                        },
                    }
                ],
            },
            self.feature(t, t["objects"]["foo"]),
        )

    def test_feature_top_level_geometry_collections_do_not_have_properties_but_second_level_geometry_collections_can(
        self,
    ):
        t = self.simple_topology(
            {
                "type": "GeometryCollection",
                "properties": {"collection": True},
                "geometries": [
                    {
                        "type": "GeometryCollection",
                        "properties": {"feature": True},
                        "geometries": [
                            {
                                "type": "Point",
                                "properties": {"geometry": True},
                                "coordinates": [0, 0],
                            }
                        ],
                    }
                ],
            }
        )
        self.assertDictEqual(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {"feature": True},
                        "geometry": {
                            "type": "GeometryCollection",
                            "geometries": [{"type": "Point", "coordinates": [0, 0]}],
                        },
                    }
                ],
            },
            self.feature(t, t["objects"]["foo"]),
        )

    def test_feature_the_object_id_is_promoted_to_feature_id(self):
        t = self.simple_topology({"id": "foo", "type": "Polygon", "arcs": [[0]]})
        self.assertEqual("foo", self.feature(t, t["objects"]["foo"])["id"])

    def test_feature_any_object_properties_are_promoted_to_feature_properties(self):
        t = self.simple_topology(
            {
                "type": "Polygon",
                "properties": {"color": "orange", "size": 42},
                "arcs": [[0]],
            }
        )
        self.assertDictEqual(
            {"color": "orange", "size": 42},
            self.feature(t, t["objects"]["foo"])["properties"],
        )

    def test_feature_the_object_id_is_optional(self):
        t = self.simple_topology({"type": "Polygon", "arcs": [[0]]})
        self.assertEqual(self.feature(t, t["objects"]["foo"]).get("id", None), None)

    def test_feature_object_properties_are_created_if_missing(self):
        t = self.simple_topology({"type": "Polygon", "arcs": [[0]]})
        self.assertDictEqual(self.feature(t, t["objects"]["foo"])["properties"], {})

    def test_feature_arcs_are_converted_to_coordinates(self):
        t = self.simple_topology({"type": "Polygon", "arcs": [[0]]})
        self.assertListEqual(
            self.feature(t, t["objects"]["foo"])["geometry"]["coordinates"],
            [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]],
        )

    def test_feature_negative_arc_indexes_indicate_reversed_coordinates(self):
        t = self.simple_topology({"type": "Polygon", "arcs": [[~0]]})
        self.assertListEqual(
            self.feature(t, t["objects"]["foo"])["geometry"]["coordinates"],
            [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]],
        )

    def test_feature_when_multiple_arc_indexes_are_specified_coordinates_are_stitched_together(
        self,
    ):
        t = self.simple_topology({"type": "LineString", "arcs": [1, 2]})
        self.assertListEqual(
            self.feature(t, t["objects"]["foo"])["geometry"]["coordinates"],
            [[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]],
        )

        t = self.simple_topology({"type": "Polygon", "arcs": [[~2, ~1]]})
        self.assertListEqual(
            self.feature(t, t["objects"]["foo"])["geometry"]["coordinates"],
            [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]],
        )

    def test_feature_unknown_geometry_types_are_converted_to_null_geometries(self):
        topology = {
            "type": "Topology",
            "transform": {"scale": [1, 1], "translate": [0, 0]},
            "objects": {
                "foo": {"id": "foo"},
                "bar": {"type": "Invalid", "properties": {"bar": 2}},
                "baz": {
                    "type": "GeometryCollection",
                    "geometries": [{"type": "Unknown", "id": "unknown"}],
                },
            },
            "arcs": [],
        }
        self.assertDictEqual(
            {"type": "Feature", "id": "foo", "properties": {}, "geometry": None},
            self.feature(topology, topology["objects"]["foo"]),
        )
        self.assertDictEqual(
            {"type": "Feature", "properties": {"bar": 2}, "geometry": None},
            self.feature(topology, topology["objects"]["bar"]),
        )
        self.assertDictEqual(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "id": "unknown",
                        "properties": {},
                        "geometry": None,
                    }
                ],
            },
            self.feature(topology, topology["objects"]["baz"]),
        )

    def test_feature_preserves_additional_dimensions_in_Point_geometries(self):
        t = {
            "type": "Topology",
            "objects": {"point": {"type": "Point", "coordinates": [1, 2, "foo"]}},
            "arcs": [],
        }
        self.assertDictEqual(
            {
                "type": "Feature",
                "properties": {},
                "geometry": {"type": "Point", "coordinates": [1, 2, "foo"]},
            },
            self.feature(t, t["objects"]["point"]),
        )

    def test_feature_preserves_additional_dimensions_in_MultiPoint_geometries(self):
        t = {
            "type": "Topology",
            "objects": {
                "points": {"type": "MultiPoint", "coordinates": [[1, 2, "foo"]]}
            },
            "arcs": [],
        }
        self.assertDictEqual(
            {
                "type": "Feature",
                "properties": {},
                "geometry": {"type": "MultiPoint", "coordinates": [[1, 2, "foo"]]},
            },
            self.feature(t, t["objects"]["points"]),
        )

    def test_feature_preserves_additional_dimensions_in_LineString_geometries(self):
        t = {
            "type": "Topology",
            "objects": {"line": {"type": "LineString", "arcs": [0]}},
            "arcs": [[[1, 2, "foo"], [3, 4, "bar"]]],
        }
        self.assertDictEqual(
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[1, 2, "foo"], [3, 4, "bar"]],
                },
            },
            self.feature(t, t["objects"]["line"]),
        )
