import unittest

from pytopojson import bounds


class BoundsTestCase(unittest.TestCase):
    def setUp(self):
        self.bbox = bounds.BoundingBox()

    def test_bounds_computes_bounding_box(self):
        foo = {"bar": {"type": "LineString", "arcs": [[0, 0], [1, 0], [0, 2], [0, 0]]}}

        self.assertCountEqual(self.bbox(foo), [0, 0, 1, 2])

    def test_bounds_considers_points_as_well_as_arcs(self):
        foo = {
            "bar": {
                "type": "MultiPoint",
                "coordinates": [[0, 0], [1, 0], [0, 2], [0, 0]],
            }
        }

        self.assertCountEqual(self.bbox(foo), [0, 0, 1, 2])
