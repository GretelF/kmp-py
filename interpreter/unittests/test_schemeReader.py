from interpreter.kmp_py import reader,scheme,schemeExceptions
from unittest import TestCase

class SchemeReader(TestCase):
    def test_string(self):
        r = reader.SchemeReader()
        obj = r.read('"hello"')
        self.assertEqual(obj.type, 'schemeString', 'schemeReader does not work')
        self.assertEqual(obj.value, 'hello', 'schemeReader does not work')
        self.assertEqual(str(obj), '"hello"', 'schemeReader does not work')

    def test_closingParenthesis(self):
        r = reader.SchemeReader()
        self.assertRaises(schemeExceptions.InvalidInputException, r.read, ')aaa')

    def test_number(self):
        r = reader.SchemeReader()
        obj = r.read('1234')
        self.assertEqual(obj.type, 'schemeNumber', 'schemeReader does not work')
        self.assertEqual(obj.value, 1234, 'schemeReader does not work')
        self.assertEqual(str(obj), '1234', 'schemeReader does not work')

    def test_symbol(self):
        r = reader.SchemeReader()
        obj = r.read('abc')
        self.assertEqual(obj.type, 'schemeSymbol', 'schemeReader does not work')
        self.assertEqual(obj.value, 'abc', 'schemeReader does not work')
        self.assertEqual(str(obj), 'abc', 'schemeReader does not work')