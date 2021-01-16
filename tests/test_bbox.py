import json
import math
import unittest

from pytopojson import bbox


class BBoxTestCase(unittest.TestCase):
    def setUp(self):
        self.bbox = bbox.BBox()

    @staticmethod
    def _load_json_file(filepath):
        with open(filepath, "r") as src:
            return json.load(src)

    def test_bbox_topology_ignores_the_existing_bbox_if_any(self):
        bbox = [1, 2, 3, 4]
        self.assertListEqual(
            self.bbox({"type": "Topology", "bbox": bbox, "objects": {}, "arcs": {}}),
            [math.inf, math.inf, -math.inf, -math.inf],
        )

    def test_bbox_topology_computes_the_bbox_for_a_quantized_topology_if_missing(self):
        topology = self._load_json_file("tests/client/topojson/polygon-q1e4.json")
        self.assertListEqual(self.bbox(topology), [0, 0, 10, 10])

    def test_bbox_topology_computes_the_bbox_for_a_non_quantized_topology_if_missing(
        self,
    ):
        topology = self._load_json_file("tests/client/topojson/polygon.json")
        self.assertListEqual(self.bbox(topology), [0, 0, 10, 10])

    def test_bbox_topology_considers_points(self):
        topology = self._load_json_file("tests/client/topojson/point.json")
        self.assertListEqual(self.bbox(topology), [0, 0, 10, 10])

    def test_bbox_topology_considers_multipoints(self):
        topology = self._load_json_file("tests/client/topojson/points.json")
        self.assertListEqual(self.bbox(topology), [0, 0, 10, 10])
