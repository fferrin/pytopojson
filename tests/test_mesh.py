from pathlib import Path
import json
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
            self.mesh(topology, {"type": None}),
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

    def test_full_json_file_same_filter(self):
        mesh_path = Path(__file__).resolve().parent / "client" / "mesh"
        topology = json.loads((mesh_path / "states-10m.json").read_text())
        actual_mesh = self.mesh(topology, topology["objects"]["states"], filt=lambda a, b: a != b)
        expected_mesh = json.loads((mesh_path / "statemesh-10m.json").read_text())
        self.assertDictEqual(actual_mesh, expected_mesh)

    def test_full_json_file_no_filter(self):
        mesh_path = Path(__file__).resolve().parent / "client" / "mesh"
        topology = json.loads((mesh_path / "states-10m.json").read_text())
        actual_mesh = self.mesh(topology, topology["objects"]["states"])
        expected_mesh = json.loads((mesh_path / "statemesh-10m.json").read_text())
        self.assertNotEqual(actual_mesh, expected_mesh)
