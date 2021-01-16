import json
import math
import unittest

from pytopojson import (
    feature,
    mesh,
    stitch,
)


class MeshTestCase(unittest.TestCase):
    def setUp(self):
        self.feature = feature.Feature()
        self.mesh = mesh.Mesh()
        self.stitch = stitch.Stitch()

    def test_mesh_ignores_null_geometries(self):
        topology = {"type": "Topology", "objects": {}, "arcs": []}

        self.assertDictEqual(
            self.mesh(topology, [{"type": None}]),
            {"type": "MultiLineString", "coordinates": []},
        )

    def test_mesh_stitches_together_two_connected_line_strings(self):
        topology = {
            "type": "Topology",
            "objects": {
                "collection": {
                    "type": "GeometryCollection",
                    "geometries": [
                        {"type": "LineString", "arcs": [0]},
                        {"type": "LineString", "arcs": [1]},
                    ],
                }
            },
            "arcs": [[[1, 0], [2, 0]], [[0, 0], [1, 0]]],
        }
        self.assertDictEqual(
            {"type": "MultiLineString", "coordinates": [[[0, 0], [1, 0], [2, 0]]]},
            self.mesh(topology, topology["objects"]["collection"]),
        )

    def test_mesh_does_not_stitch_together_two_disconnected_line_strings(self):
        topology = {
            "type": "Topology",
            "objects": {
                "collection": {
                    "type": "GeometryCollection",
                    "geometries": [
                        {"type": "LineString", "arcs": [0]},
                        {"type": "LineString", "arcs": [1]},
                    ],
                }
            },
            "arcs": [[[2, 0], [3, 0]], [[0, 0], [1, 0]]],
        }
        self.assertDictEqual(
            {
                "type": "MultiLineString",
                "coordinates": [[[2, 0], [3, 0]], [[0, 0], [1, 0]]],
            },
            self.mesh(topology, topology["objects"]["collection"]),
        )
