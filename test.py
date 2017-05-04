import pprint
import unittest
from collections import OrderedDict

from Sorstr import Sorstr


class TestSorstr(unittest.TestCase):
    def test(self):
        sorstr = Sorstr()
        sorstr.index('resources/examples/*.txt')

        query = 'is text'
        actual = sorstr.search(query)
        pprint.pformat(actual)
        expected = OrderedDict({'2.txt': {'score': 3, 'matches': {'is': 1, 'text': 2}},
                                '1.txt': {'score': 2, 'matches': {'is': 1, 'text': 2}},
                                '3.txt': {'score': 1, 'matches': {'is': 1, 'text': 1}}})
        self.assertEquals(expected, actual, query)

        query = 'is another'
        actual = sorstr.search(query)
        self.assertEquals(['2.txt'], actual, query)

        query = 'text'
        actual = sorstr.search(query)
        self.assertEquals(['2.txt', '1.txt', '3.txt'], actual, query)

        query = 'this'
        actual = sorstr.search(query)
        self.assertEquals(['3.txt', '2.txt', '1.txt'], actual, query)

        query = 'blubbergurken'
        actual = sorstr.search(query)
        self.assertEquals([], actual, query)
