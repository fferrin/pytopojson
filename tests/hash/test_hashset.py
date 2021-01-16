import unittest

from tests.hash.test_hashmap import equal, hash
from pytopojson.hash.hash import HashSet


def equal(a, b):
    return a is b


def hash(o):
    return o["hash"]


class HashSetTestCase(unittest.TestCase):
    def test_hashset_can_add_an_object(self):
        map = HashSet(10, hash, equal)
        key = {"hash": 1}

        self.assertEqual(map.add(key), True)
        self.assertEqual(map.has(key), True)

    def test_hashset_has_returns_false_when_no_key_is_found(self):
        map = HashSet(10, hash, equal)
        key = {"hash": 1}

        self.assertEqual(map.has(key), False)

    def test_hashset_when_a_hash_collision_occurs_get_checks_that_the_keys_are_equal(
        self,
    ):
        map = HashSet(10, hash, equal)
        key_1 = {"hash": 1}
        key_2 = {"hash": 1}
        key_3 = {"hash": 1}

        self.assertEqual(map.add(key_1), True)
        self.assertEqual(map.add(key_2), True)
        self.assertEqual(map.has(key_1), True)
        self.assertEqual(map.has(key_2), True)
        self.assertEqual(map.has(key_3), False)

    def test_hashset_add_returns_true(self):
        map = HashSet(10, hash, equal)
        key = {"hash": 1}

        self.assertEqual(map.add(key), True)

    def test_hashset_add_throws_an_error_when_full(self):
        # minimum size of 16
        map = HashSet(0, hash, equal)
        keys = list()

        for i in range(16):
            keys.append({"hash": i})
            map.add(keys[i])

        # replacing is okay
        for i in range(16):
            map.add(keys[i])

        with self.assertRaises(ValueError):
            map.add({"hash": 16})

    def test_hashset_the_hash_function_must_return_a_nonnegative_integer_but_can_be_greater_than_size(
        self,
    ):
        map = HashSet(10, hash, equal)
        key = {"hash": 11}

        self.assertEqual(map.has(key), False)
        self.assertEqual(map.add(key), True)
        self.assertEqual(map.has(key), True)


if __name__ == "__main__":
    unittest.main()
