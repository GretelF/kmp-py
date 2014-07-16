from interpreter.kmp_py import reader,schemeExceptions
from interpreter.kmp_py.scheme import *
from unittest import TestCase

class SchemeReader(TestCase):
    def test_string_normal(self):
        r = reader.SchemeReader()
        obj = r.read(SchemeStringStream('"hello"'))
        self.assertEqual(obj.type, 'schemeString', 'schemeReader does not work. Expected type schemeString, but got '+ obj.type)
        self.assertEqual(obj.value, 'hello', 'schemeReader does not work')
        self.assertEqual(str(obj), '"hello"', 'schemeReader does not work')

    def test_string_with_tail(self):
        r = reader.SchemeReader()
        stream = SchemeStringStream('"hello"abc')
        obj = r.read(stream)
        self.assertFalse(stream.isAtEndOfStream(), 'schemeReader does not work for Strings (does not read over closing " )')
        self.assertEqual(stream.peek(), 'a', 'schemeReader does not work for Strings (does not read over closing " )')

    def test_closingParenthesis(self):
        r = reader.SchemeReader()
        self.assertRaises(schemeExceptions.InvalidInputException, r.read, SchemeStringStream(')aaa'))

    def test_number(self):
        r = reader.SchemeReader()
        obj = r.read(SchemeStringStream('1234'))
        self.assertEqual(obj.type, 'schemeNumber', 'schemeReader does not work. Expected type schemeNumber, but got '+ obj.type)
        self.assertEqual(obj.value, 1234, 'schemeReader does not work')
        self.assertEqual(str(obj), '1234', 'schemeReader does not work')

        obj2 = r.read(SchemeStringStream('-1'))
        self.assertEqual(obj2.type, 'schemeNumber', 'schemeReader does not work for negative numbers. Expected type schemeNumber, but got '+ obj.type)
        self.assertEqual(obj2.value, -1, 'schemeReader does not work')
        self.assertEqual(str(obj2), '-1', 'schemeReader does not work')

    def test_symbol(self):
        r = reader.SchemeReader()
        obj = r.read(SchemeStringStream('abc'))
        self.assertEqual(obj.type, 'schemeSymbol', 'schemeReader does not work. Expected type schemeSymbol, but got '+ obj.type)
        self.assertEqual(obj.value, 'abc', 'schemeReader does not work')
        self.assertEqual(str(obj), 'abc', 'schemeReader does not work')

    def test_list_two_elements(self):
        r = reader.SchemeReader()
        obj = r.read(SchemeStringStream('(1 2)'))
        self.assertEqual(obj.type, 'schemeCons', 'schemeReader can not read functions. Expected schemeCons, but got '+ obj.type)
        self.assertEqual(str(obj),'(1 2)', 'schemeReader does not work for lists.')

    def test_list_three_elements(self):
        r = reader.SchemeReader()
        obj = r.read(SchemeStringStream('(1 2 "hello")'))
        self.assertEqual(obj.type, 'schemeCons', 'schemeReader can not read functions. Expected schemeCons, but got '+ obj.type)
        self.assertEqual(str(obj), '(1 2 "hello")', 'schemeReader does not work for lists')
        self.assertEqual(obj.type, 'schemeCons', 'schemeReader does not work for lists')
        self.assertEqual(obj.car.value, 1, 'schemeReader does not work for lists')                            # first list element
        self.assertEqual(obj.cdr.type, 'schemeCons', 'schemeReader does not work for lists')
        self.assertEqual(obj.cdr.car.value, 2, 'schemeReader does not work for lists')                        # second list element
        self.assertEqual(obj.cdr.cdr.type, 'schemeCons', 'schemeReader does not work for lists')
        self.assertEqual(obj.cdr.cdr.car.value, 'hello', 'schemeReader does not work for lists')              # third list element
        self.assertEqual(obj.cdr.cdr.cdr.type, 'schemeNil', 'schemeReader does not work for lists')           # final nil

    def test_list_nested(self):
        r = reader.SchemeReader()
        obj = r.read(SchemeStringStream('(define (x a b) (+ a b 1234))'))
        self.assertEqual(obj.type, 'schemeCons', 'schemeReader can not read functions. Expected schemeCons, but got '+ obj.type)
        self.assertEqual(str(obj), '(define (x a b) (+ a b 1234))')
        self.assertEqual(obj.type, 'schemeCons', 'schemeReader does not work for lists')
        self.assertEqual(obj.car.value, 'define', 'schemeReader does not work for lists')
        self.assertEqual(obj.cdr.type, 'schemeCons', 'schemeReader does not work for lists')
        self.assertEqual(obj.cdr.car.type, 'schemeCons', 'schemeReader does not work for lists')
        self.assertEqual(obj.cdr.car.car.value, 'x', 'schemeReader does not work for lists')
        self.assertEqual(obj.cdr.car.cdr.car.value, 'a', 'schemeReader does not work for lists')
        self.assertEqual(obj.cdr.car.cdr.cdr.car.value, 'b', 'schemeReader does not work for lists')
        self.assertEqual(obj.cdr.car.cdr.cdr.cdr.type, 'schemeNil', 'schemeReader does not work for lists')
        self.assertEqual(obj.cdr.cdr.type, 'schemeCons', 'schemeReader does not work for lists')
        self.assertEqual(obj.cdr.cdr.car.type, 'schemeCons', 'schemeReader does not work for lists')
        self.assertEqual(obj.cdr.cdr.car.car.value, '+', 'schemeReader does not work for lists')
        self.assertEqual(obj.cdr.cdr.car.cdr.car.value, 'a', 'schemeReader does not work for lists')
        self.assertEqual(obj.cdr.cdr.car.cdr.cdr.car.value, 'b', 'schemeReader does not work for lists')
        self.assertEqual(obj.cdr.cdr.car.cdr.cdr.cdr.car.value, 1234, 'schemeReader does not work for lists')
        self.assertEqual(obj.cdr.cdr.car.cdr.cdr.cdr.cdr.type, 'schemeNil', 'schemeReader does not work for lists')
        self.assertEqual(obj.cdr.cdr.cdr.type, 'schemeNil', 'schemeReader does not work for lists')

    def test_list_nil(self):
        r = reader.SchemeReader()
        obj = r.read(SchemeStringStream('()'))
        self.assertEqual(obj.type, 'schemeNil', 'empty list is supposed to be passed as nil')

    def test_list_broken(self):
        r = reader.SchemeReader()
        string = '(1 2 3)))))))))'
        stream = SchemeStringStream(string)
        obj = r.read(stream)
        self.assertRaises(schemeExceptions.InvalidInputException, r.read, stream)

        string = '('
        stream = SchemeStringStream(string)
        self.assertRaises(schemeExceptions.EOFException, r.read, stream)

    def test_read_function(self):
        r = reader.SchemeReader()
        string = '(define x (cons 1 (cons 2 nil)))'
        obj = r.read(SchemeStringStream(string))
        self.assertEqual(obj.type, 'schemeCons', 'schemeReader can not read functions. Expected schemeCons, but got '+ obj.type)
        self.assertEqual(str(obj),'(define x (cons 1 (cons 2 nil)))', 'schemeReader can not read functions.' )

    def test_read_string_EOF(self):
        r = reader.SchemeReader()
        string = '(cons 1 "hello)'
        self.assertRaises(schemeExceptions.EOFException, r.read, SchemeStringStream(string))

    def test_checkSyntax_whitespaces(self):
        r = reader.SchemeReader()
        string = '\n\t\t\t\t       \r\r\b\n\n'
        stream = SchemeStringStream(string)
        syntaxResult = r.checkSyntax(stream)
        self.assertTrue(syntaxResult.isBalanced(), 'stream with whitespace only should be complete')
        self.assertTrue(syntaxResult.isValid(), 'stream with whitespace only should be valid' )

    def test_checkSyntax_openingParenthesisOnly(self):
        r = reader.SchemeReader()
        string = '('
        stream = SchemeStringStream(string)
        syntaxResult = r.checkSyntax(stream)
        self.assertFalse(syntaxResult.isBalanced(), 'stream with one opening parenthesis should not be complete')
        self.assertEqual(syntaxResult.balance, 1, 'stream with one opening parenthesis should have balance 1')
        self.assertTrue(syntaxResult.isValid(), 'stream with one opening parenthesis should be valid')

    def test_checkSyntax_closingParenthesisOnly(self):
        r = reader.SchemeReader()
        string = ')'
        stream = SchemeStringStream(string)
        syntaxResult = r.checkSyntax(stream)
        self.assertFalse(syntaxResult.isBalanced(), 'stream with one closing parenthesis should not be complete')
        self.assertEqual(syntaxResult.balance, -1, 'stream with one closing parenthesis should have balance -1')
        self.assertFalse(syntaxResult.isValid(), 'stream with one closing parenthesis should not be valid')

    def test_checkSyntax_complex(self):
        r = reader.SchemeReader()
        string = '(define x (cons 1 2)))'
        stream = SchemeStringStream(string)
        syntaxResult = r.checkSyntax(stream)
        self.assertFalse(syntaxResult.isBalanced(), 'stream with one closing parenthesis should not be complete')
        self.assertEqual(syntaxResult.balance, -1, 'stream with one closing parenthesis should have balance -1')
        self.assertFalse(syntaxResult.isValid(), 'stream with one closing parenthesis should not be valid')

