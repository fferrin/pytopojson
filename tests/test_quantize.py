import json
import unittest

from pytopojson import quantize


class QuantizeTestCase(unittest.TestCase):
    def setUp(self):
        self.quantize = quantize.Quantize()

    @staticmethod
    def _load_json_file(filepath):
        with open(filepath, "r") as src:
            return json.load(src)

    def test_quantize_the_input_topology(self):
        polygon = self._load_json_file("tests/client/topojson/polygon.json")

        quantized = self._load_json_file("tests/client/topojson/polygon-q1e4.json")
        self.assertDictEqual(self.quantize(polygon, 1e4), quantized)

        quantized = self._load_json_file("tests/client/topojson/polygon-q1e5.json")
        self.assertDictEqual(self.quantize(polygon, 1e5), quantized)

    def test_quantize_ensures_that_each_arc_has_at_least_two_points(self):
        polygon = self._load_json_file("tests/client/topojson/empty.json")
        quantized = self._load_json_file("tests/client/topojson/empty-q1e4.json")
        self.assertDictEqual(self.quantize(polygon, 1e4), quantized)

    def test_quantize_preserves_the_id_bbox_and_properties_of_input_objects(self):
        polygon = self._load_json_file("tests/client/topojson/properties.json")
        quantized = self._load_json_file("tests/client/topojson/properties-q1e4.json")
        self.assertDictEqual(self.quantize(polygon, 1e4), quantized)

    def test_quantize_throws_an_error_if_n_is_not_at_least_two(self):
        topology = self._load_json_file("tests/client/topojson/polygon.json")
        with self.assertRaises(ValueError) as exc:
            self.quantize(topology, 0)
        self.assertEqual("n must be ≥2.", str(exc.exception))
        with self.assertRaises(ValueError) as exc:
            self.quantize(topology, 1.5)
        self.assertEqual("n must be ≥2.", str(exc.exception))
        with self.assertRaises(ValueError) as exc:
            self.quantize(topology)
        self.assertEqual("n must be ≥2.", str(exc.exception))
        with self.assertRaises(ValueError) as exc:
            self.quantize(topology, None)
        self.assertEqual("n must be ≥2.", str(exc.exception))
        with self.assertRaises(ValueError) as exc:
            self.quantize(topology, -2)
        self.assertEqual("n must be ≥2.", str(exc.exception))

    def test_quantize_throws_an_error_if_the_topology_is_already_quantized(self):
        topology = self._load_json_file("tests/client/topojson/polygon-q1e4.json")
        with self.assertRaises(ValueError) as exc:
            self.quantize(topology, 1e4)
        self.assertEqual("Already quantized.", str(exc.exception))

    def test_quantize_returns_a_new_topology_with_a_bounding_box(self):
        before = self._load_json_file("tests/client/topojson/polygon.json")
        before["bbox"] = None
        after = self.quantize(before, 1e4)

        quantized = self._load_json_file("tests/client/topojson/polygon-q1e4.json")
        self.assertDictEqual(after, quantized)
        self.assertListEqual(after["bbox"], [0, 0, 10, 10])
        self.assertIsNone(before["bbox"])
