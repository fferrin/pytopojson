import unittest

from pytopojson import extract


class ExtractTestCase(unittest.TestCase):
    def setUp(self):
        self.extract = extract.Extract()

    def test_extract_copies_coordinates_sequentially_into_a_buffer(self):
        topology = self.extract(
            {
                "foo": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                "bar": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
            }
        )

        self.assertCountEqual(
            topology["coordinates"], [[0, 0], [1, 0], [2, 0], [0, 0], [1, 0], [2, 0]]
        )

    def test_extract_does_not_copy_point_geometries_into_the_coordinate_buffer(self):
        topology = self.extract(
            {
                "foo": {"type": "Point", "arcs": [0, 0]},
                "bar": {"type": "MultiPoint", "arcs": [[0, 0], [1, 0], [2, 0]]},
            }
        )

        self.assertCountEqual(topology["coordinates"], [])
        self.assertCountEqual(topology["objects"]["foo"]["arcs"], [0, 0])
        self.assertCountEqual(
            topology["objects"]["bar"]["arcs"], [[0, 0], [1, 0], [2, 0]]
        )

    def test_extract_includes_closing_coordinates_in_polygons(self):
        topology = self.extract(
            {"foo": {"type": "Polygon", "arcs": [[[0, 0], [1, 0], [2, 0], [0, 0]]]}}
        )

        self.assertCountEqual(topology["coordinates"], [[0, 0], [1, 0], [2, 0], [0, 0]])

    def test_extract_represents_lines_as_contiguous_slices_of_the_coordinate_buffer(
        self,
    ):
        topology = self.extract(
            {
                "foo": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                "bar": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
            }
        )

        self.assertDictEqual(
            topology["objects"],
            {
                "foo": {"type": "LineString", "arcs": [0, 2]},
                "bar": {"type": "LineString", "arcs": [3, 5]},
            },
        )

    def test_extract_represents_rings_as_contiguous_slices_of_the_coordinate_buffer(
        self,
    ):
        topology = self.extract(
            {
                "foo": {"type": "Polygon", "arcs": [[[0, 0], [1, 0], [2, 0], [0, 0]]]},
                "bar": {"type": "Polygon", "arcs": [[[0, 0], [1, 0], [2, 0], [0, 0]]]},
            }
        )

        self.assertDictEqual(
            topology["objects"],
            {
                "foo": {"type": "Polygon", "arcs": [[0, 3]]},
                "bar": {"type": "Polygon", "arcs": [[4, 7]]},
            },
        )

    def test_extract_exposes_the_constructed_lines_and_rings_in_the_order_of_construction(
        self,
    ):
        topology = self.extract(
            {
                "line": {"type": "LineString", "arcs": [[0, 0], [1, 0], [2, 0]]},
                "multiline": {
                    "type": "MultiLineString",
                    "arcs": [[[0, 0], [1, 0], [2, 0]]],
                },
                "polygon": {
                    "type": "Polygon",
                    "arcs": [[[0, 0], [1, 0], [2, 0], [0, 0]]],
                },
            }
        )

        self.assertCountEqual(topology["lines"], [[0, 2], [3, 5]])
        self.assertCountEqual(topology["rings"], [[6, 9]])

    def test_extract_supports_nested_geometry_collections(self):
        topology = self.extract(
            {
                "foo": {
                    "type": "GeometryCollection",
                    "geometries": [
                        {
                            "type": "GeometryCollection",
                            "geometries": [
                                {"type": "LineString", "arcs": [[0, 0], [0, 1]]}
                            ],
                        }
                    ],
                }
            }
        )

        self.assertDictEqual(
            topology["objects"]["foo"],
            {
                "type": "GeometryCollection",
                "geometries": [
                    {
                        "type": "GeometryCollection",
                        "geometries": [{"type": "LineString", "arcs": [0, 1]}],
                    }
                ],
            },
        )
