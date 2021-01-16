import json
import math
import unittest

from pytopojson import neighbors


class NeighborsTestCase(unittest.TestCase):
    def setUp(self):
        self.neighbors = neighbors.Neighbors()

    def test_neighbors_returns_an_empty_array_for_objects_with_no_neighbors(self):
        """
        A-----B

        C-----D
        """
        topology = {
            "type": "Topology",
            "objects": {
                "ab": {"type": "LineString", "arcs": [0]},
                "cd": {"type": "LineString", "arcs": [1]},
            },
            "arcs": [[[0, 0], [1, 0]], [[0, 1], [1, 1]]],
        }
        self.assertListEqual(
            self.neighbors([topology["objects"]["ab"], topology["objects"]["cd"]]),
            [[], []],
        )

    def test_neighbors_returns_an_empty_array_for_empty_input(self):
        self.assertListEqual(self.neighbors([]), [])

    def test_neighbors_geometries_that_only_share_isolated_points_are_not_considered_neighbors(
        self,
    ):
        """
        A-----B-----C
        """
        topology = {
            "type": "Topology",
            "objects": {
                "ab": {"type": "LineString", "arcs": [0]},
                "bc": {"type": "LineString", "arcs": [1]},
            },
            "arcs": [[[0, 0], [1, 0]], [[1, 0], [2, 0]]],
        }
        self.assertListEqual(
            self.neighbors([topology["objects"]["ab"], topology["objects"]["bc"]]),
            [[], []],
        )

    def test_neighbors_geometries_that_share_arcs_are_considered_neighbors(self):
        """
        A-----B-----C-----D
        """
        topology = {
            "type": "Topology",
            "objects": {
                "abc": {"type": "LineString", "arcs": [0, 1]},
                "bcd": {"type": "LineString", "arcs": [1, 2]},
            },
            "arcs": [[[0, 0], [1, 0]], [[1, 0], [2, 0]], [[2, 0], [3, 0]]],
        }
        self.assertListEqual(
            self.neighbors([topology["objects"]["abc"], topology["objects"]["bcd"]]),
            [[1], [0]],
        )

    def test_neighbors_geometries_that_share_reversed_arcs_are_considered_neighbors(
        self,
    ):
        """
        A-----B-----C-----D
        """
        topology = {
            "type": "Topology",
            "objects": {
                "abc": {"type": "LineString", "arcs": [0, 1]},
                "dcb": {"type": "LineString", "arcs": [2, -2]},
            },
            "arcs": [[[0, 0], [1, 0]], [[1, 0], [2, 0]], [[3, 0], [2, 0]]],
        }
        self.assertListEqual(
            self.neighbors([topology["objects"]["abc"], topology["objects"]["dcb"]]),
            [[1], [0]],
        )

    def test_neighbors_neighbors_are_returned_in_sorted_order_by_index(self):
        """
        A-----B-----C-----D-----E-----F
        """
        topology = {
            "type": "Topology",
            "objects": {
                "abcd": {"type": "LineString", "arcs": [0, 1, 2]},
                "bcde": {"type": "LineString", "arcs": [1, 2, 3]},
                "cdef": {"type": "LineString", "arcs": [2, 3, 4]},
                "dbca": {"type": "LineString", "arcs": [-3, -2, -1]},
                "edcb": {"type": "LineString", "arcs": [-4, -3, -2]},
                "fedc": {"type": "LineString", "arcs": [-5, -4, -3]},
            },
            "arcs": [
                [[0, 0], [1, 0]],
                [[1, 0], [2, 0]],
                [[2, 0], [3, 0]],
                [[3, 0], [4, 0]],
                [[4, 0], [5, 0]],
            ],
        }
        self.assertListEqual(
            self.neighbors(
                [
                    topology["objects"]["abcd"],
                    topology["objects"]["bcde"],
                    topology["objects"]["cdef"],
                    topology["objects"]["dbca"],
                    topology["objects"]["edcb"],
                    topology["objects"]["fedc"],
                ]
            ),
            [
                [1, 2, 3, 4, 5],
                [0, 2, 3, 4, 5],
                [0, 1, 3, 4, 5],
                [0, 1, 2, 4, 5],
                [0, 1, 2, 3, 5],
                [0, 1, 2, 3, 4],
            ],
        )

    def test_neighbors_the_polygons_abcda_and_befcb_are_neighbors_but_ghig_is_not(self):
        """
         A-----B-----E     G
         |     |     |     |\
         |     |     |     | \
         |     |     |     |  \
         |     |     |     |   \
         |     |     |     |    \
         D-----C-----F     I-----H
        """
        topology = {
            "type": "Topology",
            "objects": {
                "abcda": {"type": "Polygon", "arcs": [[0, 1]]},
                "befcb": {"type": "Polygon", "arcs": [[2, -1]]},
                "ghig": {"type": "Polygon", "arcs": [[3]]},
            },
            "arcs": [
                [[1, 0], [1, 1]],
                [[1, 1], [0, 1], [0, 0], [1, 0]],
                [[1, 0], [2, 0], [2, 1], [1, 1]],
                [[3, 0], [4, 1], [3, 1], [3, 0]],
            ],
        }
        self.assertListEqual(
            self.neighbors(
                [
                    topology["objects"]["abcda"],
                    topology["objects"]["befcb"],
                    topology["objects"]["ghig"],
                ]
            ),
            [[1], [0], []],
        )

    def test_neighbors_the_polygons_abedghkja_and_bclkhifeb_are_neighbors_and_not_listed_twice(
        self,
    ):
        """
        A-----------B-----------C
        |           |           |
        |           |           |
        |     D-----E-----F     |
        |     |           |     |
        |     |           |     |
        |     G-----H-----I     |
        |           |           |
        |           |           |
        J-----------K-----------L
        """
        topology = {
            "type": "Topology",
            "objects": {
                "abdeghkja": {"type": "Polygon", "arcs": [[0, 1, 2, 3]]},
                "bclkhifeb": {"type": "Polygon", "arcs": [[4, -3, 5, -1]]},
            },
            "arcs": [
                [[2, 0], [2, 1]],
                [[2, 1], [1, 1], [1, 2], [2, 2]],
                [[2, 2], [2, 3]],
                [[2, 3], [0, 3], [0, 0], [2, 0]],
                [[2, 0], [4, 0], [4, 3], [2, 3]],
                [[2, 2], [3, 2], [3, 1], [2, 1]],
            ],
        }
        self.assertListEqual(
            self.neighbors(
                [topology["objects"]["abdeghkja"], topology["objects"]["bclkhifeb"]]
            ),
            [[1], [0]],
        )
