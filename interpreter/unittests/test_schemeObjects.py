from unittest import TestCase
from interpreter.kmp_py import scheme

__author__ = 'maria'


class TestSchemeFalse(TestCase):

    def test_schemeFalse(self):
        first = scheme.SchemeFalse()
        second = scheme.SchemeFalse()
        self.assertIs(first, second, 'schemeFalse is no singleton')

    def test_schemeFalse_str(self):
        false = scheme.SchemeFalse()
        self.assertEqual(str(false), '#f', 'schemeFalse function __str__ does not work')


class TestSchemeTrue(TestCase):
    def test_schemeTrue(self):
        first = scheme.SchemeTrue()
        second = scheme.SchemeTrue()
        self.assertIs(first, second, 'schemeTrue is no singleton')

    def test_schemeTrue_equals_schemeFalse(self):
        f = scheme.SchemeFalse()
        t = scheme.SchemeTrue()
        self.assertNotEqual(t, f, "schemeTrue and schemeFalse should not be equal!")

    def test_schemeTrue_str(self):
        true = scheme.SchemeTrue()
        self.assertEqual(str(true), '#t', 'schemeTrue function __str__ does not work')


class TestSchemeNil(TestCase):
    def test_schemeNil(self):
        firstNil = scheme.SchemeNil()
        secondNil = scheme.SchemeNil()

        self.assertIs(firstNil, secondNil, 'schemeNil should be singleton')

    def test_schemeNil_str(self):
        nil = scheme.SchemeNil()
        self.assertEqual(str(nil), '()', 'schemeSymbol function __str__ does not work')


class TestSchemeString(TestCase):
    def test_schemeString(self):
        string = scheme.SchemeString('Hello')
        self.assertEqual(string.value, 'Hello', 'schemeString does not work')

    def test_schemeString_str(self):
        string = scheme.SchemeString('hello')
        self.assertEqual(str(string), '"hello"', 'schemeString function __str__ does not work')


class TestSchemeSymbol(TestCase):
    def test_schemeSymbol(self):
        firstSymbol = scheme.SchemeSymbol('x')
        secondSymbol = scheme.SchemeSymbol('y')
        self.assertEqual(firstSymbol.value, 'x', 'schemeSymbol does not work')
        self.assertIsNot(firstSymbol, secondSymbol, 'schemeSymbol with different values should not be same')

    def test_schemeSymbol_sameInstance(self):
        firstSymbol = scheme.SchemeSymbol('x')
        secondSymbol = scheme.SchemeSymbol('x')
        self.assertIs(firstSymbol, secondSymbol, 'schemeSymbol with same value should be same')

    def test_schemeSymbol_str(self):
        symbol = scheme.SchemeSymbol('x')
        self.assertEqual(str(symbol), 'x', 'schemeSymbol function __str__ does not work')


class TestSchemeNumber(TestCase):
    def test_schemeNumber(self):
        x = scheme.SchemeNumber(3)
        y = scheme.SchemeNumber(3)

        self.assertEqual(x.value, 3, 'schemeNumber does not work')
        self.assertEqual(x, y, 'equal schemeNumbers are not equal')

    def test_schemeNumber_sameInstance(self):
        x = scheme.SchemeNumber(3)
        y = scheme.SchemeNumber(3)
        self.assertIs(x, y, 'same schemeNumbers are not same')

    def test_schemeNumber_str(self):
        x = scheme.SchemeNumber(3)
        self.assertEqual(str(x), '3', 'schemeNumber function __str__ does not work')


class TestSchemeCons(TestCase):
    def test_schemeCons_equal(self):
        first = scheme.SchemeCons('hello', 'world')
        second = scheme.SchemeCons('1', 2)
        third = scheme.SchemeCons('hello', 'world')

        self.assertIsNot(first, second, 'schemeCons should not be singleton')
        self.assertNotEqual(first, second, 'schemeCons function "__eq__" does not work: not equal schemeCons are equal')
        self.assertEqual(first, third, 'schemeCons function "__eq__" does not work: equal schemeCons are not equal')

    def test_schemeCons_str(self):
        car = scheme.SchemeString('hello')
        cdr = scheme.SchemeNumber(3)
        cons = scheme.SchemeCons(car, cdr)
        self.assertEqual(str(cons), '("hello" . 3)', 'schemeString function __str__ does not work')

    def test_schemeCons_car_cdr(self):
        innerCar = scheme.SchemeString('Hello')
        innerCdr = scheme.SchemeNumber(3)
        outerCar = scheme.SchemeNumber(3)

        outerCdr = scheme.SchemeCons(innerCar, innerCdr)
        outerCons = scheme.SchemeCons(outerCar, outerCdr)

        self.assertEqual(outerCons.car.value, 3, 'schemeCons car does not work')
        self.assertEqual(outerCons.cdr.car.value, 'Hello', 'nested schemeCons do not work')
        self.assertEqual(outerCons.cdr.cdr.value, 3, 'nested schemeCons do not work')


