import unittest

from pytopojson import prequantize


class PrequantizeTestCase(unittest.TestCase):
    def setUp(self):
        self.prequantize = prequantize.Prequantize()

    def test_prequantize_returns_the_quantization_transform(self):
        quantize = self.prequantize({}, [0, 0, 1, 1], 1e4)

        self.assertDictEqual(
            quantize, {"scale": [1 / 9999, 1 / 9999], "translate": [0, 0]}
        )

    def test_prequantize_converts_coordinates_to_fixed_precision(self):
        objects = {
            "foo": {"type": "LineString", "arcs": [[0, 0], [1, 0], [0, 1], [0, 0]]}
        }

        self.prequantize(objects, [0, 0, 1, 1], 1e4)
        self.assertCountEqual(
            objects["foo"]["arcs"], [[0, 0], [9999, 0], [0, 9999], [0, 0]]
        )

    def test_prequantize_observes_the_quantization_parameter(self):
        objects = {
            "foo": {"type": "LineString", "arcs": [[0, 0], [1, 0], [0, 1], [0, 0]]}
        }

        self.prequantize(objects, [0, 0, 1, 1], 10)
        self.assertCountEqual(objects["foo"]["arcs"], [[0, 0], [9, 0], [0, 9], [0, 0]])

    def test_prequantize_observes_the_bounding_box(self):
        objects = {
            "foo": {"type": "LineString", "arcs": [[0, 0], [1, 0], [0, 1], [0, 0]]}
        }

        self.prequantize(objects, [-1, -1, 2, 2], 10)
        self.assertCountEqual(objects["foo"]["arcs"], [[3, 3], [6, 3], [3, 6], [3, 3]])

    def test_prequantize_applies_to_points_as_well_as_arcs(self):
        objects = {
            "foo": {
                "type": "MultiPoint",
                "coordinates": [[0, 0], [1, 0], [0, 1], [0, 0]],
            }
        }

        self.prequantize(objects, [0, 0, 1, 1], 1e4)
        self.assertCountEqual(
            objects["foo"]["coordinates"], [[0, 0], [9999, 0], [0, 9999], [0, 0]]
        )

    def test_prequantize_skips_coincident_points_in_lines(self):
        objects = {
            "foo": {
                "type": "LineString",
                "arcs": [[0, 0], [0.9, 0.9], [1.1, 1.1], [2, 2]],
            }
        }

        self.prequantize(objects, [0, 0, 2, 2], 3)
        self.assertCountEqual(objects["foo"]["arcs"], [[0, 0], [1, 1], [2, 2]])

    def test_prequantize_skips_coincident_points_in_polygons(self):
        objects = {
            "foo": {
                "type": "Polygon",
                "arcs": [[[0, 0], [0.9, 0.9], [1.1, 1.1], [2, 2], [0, 0]]],
            }
        }

        self.prequantize(objects, [0, 0, 2, 2], 3)
        self.assertCountEqual(
            objects["foo"]["arcs"], [[[0, 0], [1, 1], [2, 2], [0, 0]]]
        )

    def test_prequantize_does_not_skip_coincident_points_in_points(self):
        objects = {
            "foo": {
                "type": "MultiPoint",
                "coordinates": [[0, 0], [0.9, 0.9], [1.1, 1.1], [2, 2], [0, 0]],
            }
        }

        self.prequantize(objects, [0, 0, 2, 2], 3)
        self.assertCountEqual(
            objects["foo"]["coordinates"], [[0, 0], [1, 1], [1, 1], [2, 2], [0, 0]]
        )

    def test_prequantize_includes_closing_point_in_degenerate_lines(self):
        objects = {"foo": {"type": "LineString", "arcs": [[1, 1], [1, 1], [1, 1]]}}

        self.prequantize(objects, [0, 0, 2, 2], 3)
        self.assertCountEqual(objects["foo"]["arcs"], [[1, 1], [1, 1]])

    def test_prequantize_includes_closing_point_in_degenerate_polygons(self):
        objects = {
            "foo": {
                "type": "Polygon",
                "arcs": [[[0.9, 1], [1.1, 1], [1.01, 1], [0.9, 1]]],
            }
        }

        self.prequantize(objects, [0, 0, 2, 2], 3)
        self.assertCountEqual(
            objects["foo"]["arcs"], [[[1, 1], [1, 1], [1, 1], [1, 1]]]
        )
