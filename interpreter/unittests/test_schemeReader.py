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

        obj2 = r.read('-1')
        self.assertEqual(obj2.type, 'schemeNumber', 'schemeReader does not work for negative numbers')
        self.assertEqual(obj2.value, -1, 'schemeReader does not work')
        self.assertEqual(str(obj2), '-1', 'schemeReader does not work')

    def test_symbol(self):
        r = reader.SchemeReader()
        obj = r.read('abc')
        self.assertEqual(obj.type, 'schemeSymbol', 'schemeReader does not work')
        self.assertEqual(obj.value, 'abc', 'schemeReader does not work')
        self.assertEqual(str(obj), 'abc', 'schemeReader does not work')

    def test_list(self):
        r = reader.SchemeReader()
        obj = r.read('(1 2 "hello")')
        self.assertEqual(str(obj), '(1 2 "hello")', 'schemeReader does not work for lists')
        self.assertEqual(obj.type, 'schemeCons', 'schemeReader does not work for lists')
        self.assertEqual(obj.car.value, 1, 'schemeReader does not work for lists')                            # first list element
        self.assertEqual(obj.cdr.type, 'schemeCons', 'schemeReader does not work for lists')
        self.assertEqual(obj.cdr.car.value, 2, 'schemeReader does not work for lists')                        # second list element
        self.assertEqual(obj.cdr.cdr.type, 'schemeCons', 'schemeReader does not work for lists')
        self.assertEqual(obj.cdr.cdr.car.value, 'hello', 'schemeReader does not work for lists')              # third list element
        self.assertEqual(obj.cdr.cdr.cdr.type, 'schemeNil', 'schemeReader does not work for lists')           # final nil

