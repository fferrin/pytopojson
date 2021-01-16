import unittest

from pytopojson import transform


class TransformTestCase(unittest.TestCase):
    def setUp(self):
        self.transform = transform.Transform()

    def test_transform_topology_returns_the_identity_function_if_transform_is_undefined(
        self,
    ):
        transform = self.transform(None)
        point = dict()
        self.assertDictEqual(transform(point), point)

    def test_transform_topology_returns_a_point_transform_function_if_transform_is_defined(
        self,
    ):
        transform = self.transform({"scale": [2, 3], "translate": [4, 5]})
        self.assertListEqual(transform([6, 7]), [16, 26])

    def test_transform_point_returns_a_new_point(self):
        transform = self.transform({"scale": [2, 3], "translate": [4, 5]})
        point = [6, 7]
        self.assertListEqual(transform(point), [16, 26])
        self.assertListEqual(point, [6, 7])

    def test_transform_point_preserves_extra_dimensions(self):
        transform = self.transform({"scale": [2, 3], "translate": [4, 5]})
        self.assertListEqual(transform([6, 7, 42]), [16, 26, 42])
        self.assertListEqual(transform([6, 7, "foo"]), [16, 26, "foo"])
        self.assertListEqual(transform([6, 7, "foo", 42]), [16, 26, "foo", 42])

    def test_transform_point_transforms_individual_points(self):
        transform = self.transform({"scale": [2, 3], "translate": [4, 5]})
        self.assertListEqual(transform([1, 2]), [6, 11])
        self.assertListEqual(transform([3, 4]), [10, 17])
        self.assertListEqual(transform([5, 6]), [14, 23])

    def test_transform_point_index_transforms_delta_encoded_arcs(self):
        transform = self.transform({"scale": [2, 3], "translate": [4, 5]})
        self.assertListEqual(transform([1, 2], 0), [6, 11])
        self.assertListEqual(transform([3, 4], 1), [12, 23])
        self.assertListEqual(transform([5, 6], 2), [22, 41])
        self.assertListEqual(transform([1, 2], 3), [24, 47])
        self.assertListEqual(transform([3, 4], 4), [30, 59])
        self.assertListEqual(transform([5, 6], 5), [40, 77])

    def test_transform_point_index_transforms_multiple_delta_encoded_arcs(self):
        transform = self.transform({"scale": [2, 3], "translate": [4, 5]})
        self.assertListEqual(transform([1, 2], 0), [6, 11])
        self.assertListEqual(transform([3, 4], 1), [12, 23])
        self.assertListEqual(transform([5, 6], 2), [22, 41])
        self.assertListEqual(transform([1, 2], 0), [6, 11])
        self.assertListEqual(transform([3, 4], 1), [12, 23])
        self.assertListEqual(transform([5, 6], 2), [22, 41])
