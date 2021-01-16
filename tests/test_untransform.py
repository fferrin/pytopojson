import unittest

from pytopojson import untransform


class UntransformTestCase(unittest.TestCase):
    def setUp(self):
        self.untransform = untransform.Untransform()

    def test_untransform_topology_returns_the_identity_function_if_transform_is_undefined(
        self,
    ):
        untransform = self.untransform(None)
        point = dict()
        self.assertDictEqual(untransform(point), point)

    def test_untransform_topology_returns_a_point_transform_function_if_transform_is_defined(
        self,
    ):
        untransform = self.untransform({"scale": [2, 3], "translate": [4, 5]})
        self.assertListEqual(untransform([16, 26]), [6, 7])

    def test_untransform_point_returns_a_new_point(self):
        untransform = self.untransform({"scale": [2, 3], "translate": [4, 5]})
        point = [16, 26]
        self.assertListEqual(untransform(point), [6, 7])
        self.assertListEqual(point, [16, 26])

    def test_untransform_point_preserves_extra_dimensions(self):
        untransform = self.untransform({"scale": [2, 3], "translate": [4, 5]})
        self.assertListEqual(untransform([16, 26, 42]), [6, 7, 42])
        self.assertListEqual(untransform([16, 26, "foo"]), [6, 7, "foo"])
        self.assertListEqual(untransform([16, 26, "foo", 42]), [6, 7, "foo", 42])

    def test_untransform_point_untransforms_individual_points(self):
        untransform = self.untransform({"scale": [2, 3], "translate": [4, 5]})
        self.assertListEqual(untransform([6, 11]), [1, 2])
        self.assertListEqual(untransform([10, 17]), [3, 4])
        self.assertListEqual(untransform([14, 23]), [5, 6])

    def test_untransform_point_index_untransforms_delta_encoded_arcs(self):
        untransform = self.untransform({"scale": [2, 3], "translate": [4, 5]})
        self.assertListEqual(untransform([6, 11], 0), [1, 2])
        self.assertListEqual(untransform([12, 23], 1), [3, 4])
        self.assertListEqual(untransform([22, 41], 2), [5, 6])
        self.assertListEqual(untransform([24, 47], 3), [1, 2])
        self.assertListEqual(untransform([30, 59], 4), [3, 4])
        self.assertListEqual(untransform([40, 77], 5), [5, 6])

    def test_untransform_point_index_untransforms_multiple_delta_encoded_arcs(self):
        untransform = self.untransform({"scale": [2, 3], "translate": [4, 5]})
        self.assertListEqual(untransform([6, 11], 0), [1, 2])
        self.assertListEqual(untransform([12, 23], 1), [3, 4])
        self.assertListEqual(untransform([22, 41], 2), [5, 6])
        self.assertListEqual(untransform([6, 11], 0), [1, 2])
        self.assertListEqual(untransform([12, 23], 1), [3, 4])
        self.assertListEqual(untransform([22, 41], 2), [5, 6])
