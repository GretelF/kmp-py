from interpreter.kmp_py import reader
from unittest import TestCase

class SchemeReader(TestCase):
    def test_string(self):
        r = reader.SchemeReader()
        obj = r.read('"hello"')
        self.assertEqual(obj.type, 'schemeString', 'schemeReader does not work')
        self.assertEqual(obj.value, 'hello', 'schemeReader does not work')
        self.assertEqual(str(obj), '"hello"', 'schemeReader does not work')