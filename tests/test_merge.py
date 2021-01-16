import json
import math
import unittest

from pytopojson import merge


class MergeTestCase(unittest.TestCase):
    def setUp(self):
        self.merge = merge.Merge()

    def test_merge_ignores_null_geometries(self):
        topology = {"type": "Topology", "objects": {}, "arcs": []}

        self.assertDictEqual(
            self.merge(topology, [{"type": None}]),
            {"type": "MultiPolygon", "coordinates": []},
        )

    def test_merge_stitches_together_two_side_by_side_polygons(self):
        """
        +----+----+            +----+----+
        |    |    |            |         |
        |    |    |    ==>     |         |
        |    |    |            |         |
        +----+----+            +----+----+
        """
        topology = {
            "type": "Topology",
            "objects": {
                "collection": {
                    "type": "GeometryCollection",
                    "geometries": [
                        {"type": "Polygon", "arcs": [[0, 1]]},
                        {"type": "Polygon", "arcs": [[-1, 2]]},
                    ],
                }
            },
            "arcs": [
                [[1, 1], [1, 0]],
                [[1, 0], [0, 0], [0, 1], [1, 1]],
                [[1, 1], [2, 1], [2, 0], [1, 0]],
            ],
        }

        self.assertDictEqual(
            {
                "type": "MultiPolygon",
                "coordinates": [
                    [[[1, 0], [0, 0], [0, 1], [1, 1], [2, 1], [2, 0], [1, 0]]]
                ],
            },
            self.merge(topology, topology["objects"]["collection"]["geometries"]),
        )

    def test_merge_stitches_together_geometry_collections(self):
        """
        +----+----+            +----+----+
        |    |    |            |         |
        |    |    |    ==>     |         |
        |    |    |            |         |
        +----+----+            +----+----+
        """
        topology = {
            "type": "Topology",
            "objects": {
                "collection": {
                    "type": "GeometryCollection",
                    "geometries": [
                        {"type": "Polygon", "arcs": [[0, 1]]},
                        {"type": "Polygon", "arcs": [[-1, 2]]},
                    ],
                }
            },
            "arcs": [
                [[1, 1], [1, 0]],
                [[1, 0], [0, 0], [0, 1], [1, 1]],
                [[1, 1], [2, 1], [2, 0], [1, 0]],
            ],
        }
        self.assertDictEqual(
            {
                "type": "MultiPolygon",
                "coordinates": [
                    [[[1, 0], [0, 0], [0, 1], [1, 1], [2, 1], [2, 0], [1, 0]]]
                ],
            },
            self.merge(topology, [topology["objects"]["collection"]]),
        )

    def test_merge_does_not_stitch_together_two_separated_polygons(self):
        """
        +----+ +----+            +----+ +----+
        |    | |    |            |    | |    |
        |    | |    |    ==>     |    | |    |
        |    | |    |            |    | |    |
        +----+ +----+            +----+ +----+
        """
        topology = {
            "type": "Topology",
            "objects": {
                "collection": {
                    "type": "GeometryCollection",
                    "geometries": [
                        {"type": "Polygon", "arcs": [[0]]},
                        {"type": "Polygon", "arcs": [[1]]},
                    ],
                }
            },
            "arcs": [
                [[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]],
                [[2, 0], [2, 1], [3, 1], [3, 0], [2, 0]],
            ],
        }
        self.assertDictEqual(
            {
                "type": "MultiPolygon",
                "coordinates": [
                    [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]],
                    [[[2, 0], [2, 1], [3, 1], [3, 0], [2, 0]]],
                ],
            },
            self.merge(topology, topology["objects"]["collection"]["geometries"]),
        )

    def test_merge_does_not_stitch_together_a_polygon_and_its_hole(self):
        """
        +-----------+            +-----------+
        |           |            |           |
        |   +---+   |    ==>     |   +---+   |
        |   |   |   |            |   |   |   |
        |   +---+   |            |   +---+   |
        |           |            |           |
        +-----------+            +-----------+
        """
        topology = {
            "type": "Topology",
            "objects": {
                "collection": {
                    "type": "GeometryCollection",
                    "geometries": [{"type": "Polygon", "arcs": [[0], [1]]}],
                }
            },
            "arcs": [
                [[0, 0], [0, 3], [3, 3], [3, 0], [0, 0]],
                [[1, 1], [2, 1], [2, 2], [1, 2], [1, 1]],
            ],
        }
        self.assertDictEqual(
            {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [[0, 0], [0, 3], [3, 3], [3, 0], [0, 0]],
                        [[1, 1], [2, 1], [2, 2], [1, 2], [1, 1]],
                    ]
                ],
            },
            self.merge(topology, topology["objects"]["collection"]["geometries"]),
        )

    def test_merge_stitches_together_a_polygon_surrounding_another_polygon(self):
        """
        +-----------+            +-----------+
        |           |            |           |
        |   +---+   |    ==>     |           |
        |   |   |   |            |           |
        |   +---+   |            |           |
        |           |            |           |
        +-----------+            +-----------+
        """
        topology = {
            "type": "Topology",
            "objects": {
                "collection": {
                    "type": "GeometryCollection",
                    "geometries": [
                        {"type": "Polygon", "arcs": [[0], [1]]},
                        {"type": "Polygon", "arcs": [[-2]]},
                    ],
                }
            },
            "arcs": [
                [[0, 0], [0, 3], [3, 3], [3, 0], [0, 0]],
                [[1, 1], [2, 1], [2, 2], [1, 2], [1, 1]],
            ],
        }
        self.assertDictEqual(
            {
                "type": "MultiPolygon",
                "coordinates": [[[[0, 0], [0, 3], [3, 3], [3, 0], [0, 0]]]],
            },
            self.merge(topology, topology["objects"]["collection"]["geometries"]),
        )

    def test_merge_stitches_together_two_side_by_side_polygons_with_holes(self):
        """
        +-----------+-----------+            +-----------+-----------+
        |           |           |            |                       |
        |   +---+   |   +---+   |    ==>     |   +---+       +---+   |
        |   |   |   |   |   |   |            |   |   |       |   |   |
        |   +---+   |   +---+   |            |   +---+       +---+   |
        |           |           |            |                       |
        +-----------+-----------+            +-----------+-----------+
        """
        topology = {
            "type": "Topology",
            "objects": {
                "collection": {
                    "type": "GeometryCollection",
                    "geometries": [
                        {"type": "Polygon", "arcs": [[0, 1], [2]]},
                        {"type": "Polygon", "arcs": [[-1, 3], [4]]},
                    ],
                }
            },
            "arcs": [
                [[3, 3], [3, 0]],
                [[3, 0], [0, 0], [0, 3], [3, 3]],
                [[1, 1], [2, 1], [2, 2], [1, 2], [1, 1]],
                [[3, 3], [6, 3], [6, 0], [3, 0]],
                [[4, 1], [5, 1], [5, 2], [4, 2], [4, 1]],
            ],
        }
        self.assertDictEqual(
            {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [[3, 0], [0, 0], [0, 3], [3, 3], [6, 3], [6, 0], [3, 0]],
                        [[1, 1], [2, 1], [2, 2], [1, 2], [1, 1]],
                        [[4, 1], [5, 1], [5, 2], [4, 2], [4, 1]],
                    ]
                ],
            },
            self.merge(topology, topology["objects"]["collection"]["geometries"]),
        )

    def test_merge_stitches_together_two_horseshoe_polygons_creating_a_hole(self):
        """
        +-------+-------+            +-------+-------+
        |       |       |            |               |
        |   +---+---+   |    ==>     |   +---+---+   |
        |   |       |   |            |   |       |   |
        |   +---+---+   |            |   +---+---+   |
        |       |       |            |               |
        +-------+-------+            +-------+-------+
        """
        topology = {
            "type": "Topology",
            "objects": {
                "collection": {
                    "type": "GeometryCollection",
                    "geometries": [
                        {"type": "Polygon", "arcs": [[0, 1, 2, 3]]},
                        {"type": "Polygon", "arcs": [[-3, 4, -1, 5]]},
                    ],
                }
            },
            "arcs": [
                [[2, 3], [2, 2]],
                [[2, 2], [1, 2], [1, 1], [2, 1]],
                [[2, 1], [2, 0]],
                [[2, 0], [0, 0], [0, 3], [2, 3]],
                [[2, 1], [3, 1], [3, 2], [2, 2]],
                [[2, 3], [4, 3], [4, 0], [2, 0]],
            ],
        }
        self.assertDictEqual(
            {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [[2, 0], [0, 0], [0, 3], [2, 3], [4, 3], [4, 0], [2, 0]],
                        [[2, 2], [1, 2], [1, 1], [2, 1], [3, 1], [3, 2], [2, 2]],
                    ]
                ],
            },
            self.merge(topology, topology["objects"]["collection"]["geometries"]),
        )

    def test_merge_stitches_together_two_horseshoe_polygons_surrounding_two_other_polygons(
        self,
    ):
        """
        +-------+-------+            +-------+-------+
        |       |       |            |               |
        |   +---+---+   |    ==>     |               |
        |   |   |   |   |            |               |
        |   +---+---+   |            |               |
        |       |       |            |               |
        +-------+-------+            +-------+-------+
        """
        topology = {
            "type": "Topology",
            "objects": {
                "collection": {
                    "type": "GeometryCollection",
                    "geometries": [
                        {"type": "Polygon", "arcs": [[0, 1, 2, 3]]},
                        {"type": "Polygon", "arcs": [[-3, 4, -1, 5]]},
                        {"type": "Polygon", "arcs": [[6, -2]]},
                        {"type": "Polygon", "arcs": [[-7, -5]]},
                    ],
                }
            },
            "arcs": [
                [[2, 3], [2, 2]],
                [[2, 2], [1, 2], [1, 1], [2, 1]],
                [[2, 1], [2, 0]],
                [[2, 0], [0, 0], [0, 3], [2, 3]],
                [[2, 1], [3, 1], [3, 2], [2, 2]],
                [[2, 3], [4, 3], [4, 0], [2, 0]],
                [[2, 2], [2, 1]],
            ],
        }
        self.assertDictEqual(
            {
                "type": "MultiPolygon",
                "coordinates": [
                    [[[2, 0], [0, 0], [0, 3], [2, 3], [4, 3], [4, 0], [2, 0]]]
                ],
            },
            self.merge(topology, topology["objects"]["collection"]["geometries"]),
        )
