import unittest

from Sorstr import Sorstr


class TestSorstr(unittest.TestCase):
    def test(self):
        sorstr = Sorstr()
        sorstr.index('resources/*.txt')

        query = 'is text'
        result = sorstr.search(query)
        self.assertEquals(['resources/1.txt', 'resources/2.txt', 'resources/3.txt'], result,
                          'Wrong result for "{}"'.format(query))

        query = 'is another'
        result = sorstr.search(query)
        self.assertEquals(['resources/2.txt'], result, 'Wrong result for "{}"'.format(query))

        query = 'Is Another'
        result = sorstr.search(query)
        self.assertEquals(['resources/2.txt'], result, 'Wrong result for "{}"'.format(query))

        query = 'text'
        result = sorstr.search(query)
        self.assertEquals(['resources/1.txt', 'resources/2.txt', 'resources/3.txt'], result,
                          'Wrong result for "{}"'.format(query))

        query = 'blubbergurken'
        result = sorstr.search(query)
        self.assertEquals([], result, 'Wrong result for "{}"'.format(query))

        query = 'text blubbergurken'
        result = sorstr.search(query)
        self.assertEquals([], result, 'Wrong result for "{}"'.format(query))
