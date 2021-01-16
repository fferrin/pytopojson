import unittest

from pytopojson.hash.hash import HashMap


def equal(a, b):
    return a is b


def hash(o):
    return o["hash"]


class HashMapTestCase(unittest.TestCase):
    def test_hashmap_can_get_an_object_by_key(self):
        map = HashMap(10, hash, equal)
        key = {"hash": 1}
        map.set(key, 42)

        self.assertEqual(map.get(key), 42)

    def test_hashmap_get_returns_undefined_when_no_key_is_found(self):
        map = HashMap(10, hash, equal)
        key = {"hash": 1}

        self.assertEqual(map.get(key), None)

    def test_hashmap_get_returns_the_missing_value_when_no_key_is_found(self):
        map = HashMap(10, hash, equal)
        key = {"hash": 1}

        self.assertEqual(map.get(key, 42), 42)

    def test_hashmap_when_a_hash_collision_occurs_get_checks_that_the_keys_are_equal(
        self,
    ):
        map = HashMap(10, hash, equal)
        key_1 = {"hash": 1}
        key_2 = {"hash": 1}
        key_3 = {"hash": 1}

        map.set(key_1, "A")
        map.set(key_2, "B")

        self.assertEqual(map.get(key_1), "A")
        self.assertEqual(map.get(key_2), "B")
        self.assertEqual(map.get(key_3), None)

    def test_hashmap_can_set_an_object_by_key(self):
        map = HashMap(10, hash, equal)
        key = {"hash": 1}

        map.set(key, 42)

        self.assertEqual(map.get(key), 42)

    def test_hashmap_can_set_an_object_by_key_if_not_already_set(self):
        map = HashMap(10, hash, equal)
        key = {"hash": 1}

        self.assertEqual(map.maybe_set(key, 42), 42)
        self.assertEqual(map.get(key), 42)
        self.assertEqual(map.maybe_set(key, 43), 42)
        self.assertEqual(map.get(key), 42)

    def test_hashmap_set_returns_the_set_value(self):
        map = HashMap(10, hash, equal)
        key = {"hash": 1}

        self.assertEqual(map.set(key, 42), 42)

    def test_hashmap_set_throws_an_error_when_full(self):
        # minimum size of 16
        map = HashMap(0, hash, equal)
        keys = list()

        for i in range(16):
            keys.append({"hash": i})
            map.set(keys[i], True)

        # replacing is okay
        for i in range(16):
            map.set(keys[i], True)

        with self.assertRaises(ValueError):
            map.set({"hash": 16}, True)

    def test_hashmap_when_a_hash_collision_occurs_set_checks_that_the_keys_are_equal(
        self,
    ):
        map = HashMap(10, hash, equal)
        key_1 = {"hash": 1}
        key_2 = {"hash": 1}
        key_3 = {"hash": 1}

        self.assertEqual(map.set(key_1, "A"), "A")
        self.assertEqual(map.set(key_2, "B"), "B")
        self.assertEqual(map.get(key_1), "A")
        self.assertEqual(map.get(key_2), "B")
        self.assertEqual(map.get(key_1), "A")
        self.assertEqual(map.get(key_3), None)

    def test_hashmap_the_hash_function_must_return_a_nonnegative_integer_but_can_be_greater_than_size(
        self,
    ):
        map = HashMap(10, hash, equal)
        key = {"hash": 11}

        self.assertEqual(map.get(key), None)
        self.assertEqual(map.set(key, 42), 42)
        self.assertEqual(map.get(key), 42)
