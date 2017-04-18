import unittest

from Sorstr import Sorstr


class TestSorstr(unittest.TestCase):
    def test(self):
        sorstr = Sorstr()
        sorstr.index('resources/*.txt')
        result = sorstr.search('is text')
        result.sort()
        self.assertEquals(['resources/1.txt', 'resources/2.txt'], result)

        result = sorstr.search('is another')
        self.assertEquals(['resources/2.txt'], result)

        result = sorstr.search('text')
        self.assertEquals(['resources/1.txt', 'resources/2.txt'], result)

        result = sorstr.search('this')
        self.assertEquals(['resources/1.txt'], result)
