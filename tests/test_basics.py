__author__ = 'kj'

import unittest

class BasicsTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_iterable(self):
        from collections import Iterable
        tuple_, set_, list_, dict_ = tuple(), set(), list(), dict()
        self.assertIsInstance(tuple_, Iterable)
        self.assertIsInstance(set_, Iterable)
        self.assertIsInstance(list_, Iterable)
        self.assertIsInstance(dict_, Iterable)