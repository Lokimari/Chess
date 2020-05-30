import unittest
from datatypes import Vec2

class DataTypesTests(unittest.TestCase):
    def test_add_two_vectors(self):
        v1 = Vec2(2, 2)
        v2 = Vec2(3, 3)

        actual = v1 + v2
        expected = Vec2(5, 5)

        self.assertEqual(actual, expected)
