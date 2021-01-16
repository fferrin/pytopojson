import unittest

from pytopojson import delta


class DeltaTestCase(unittest.TestCase):
    def setUp(self):
        self.delta = delta.Delta()

    def test_delta_converts_arcs_to_delta_encoding(self):
        d = self.delta([[[0, 0], [9999, 0], [0, 9999], [0, 0]]])

        self.assertCountEqual(d, [[[0, 0], [9999, 0], [-9999, 9999], [0, -9999]]])

    def test_delta_skips_coincident_points(self):
        d = self.delta([[[0, 0], [9999, 0], [9999, 0], [0, 9999], [0, 0]]])

        self.assertCountEqual(d, [[[0, 0], [9999, 0], [-9999, 9999], [0, -9999]]])

    def test_delta_preserves_at_least_two_positions(self):
        d = self.delta(
            [[[12345, 12345], [12345, 12345], [12345, 12345], [12345, 12345]]]
        )

        self.assertCountEqual(d, [[[12345, 12345], [0, 0]]])
