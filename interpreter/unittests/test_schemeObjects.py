from unittest import TestCase
from interpreter.kmp_py import scheme

__author__ = 'maria'


class TestSchemeFalse(TestCase):

    def test_schemeFalse(self):
        first = scheme.schemeFalse()
        second = scheme.schemeFalse()
        self.assertIs(first, second, 'schemeFalse is no singleton')

class TestSchemeTrue(TestCase):
     def test_schemeTrue(self):
        first = scheme.schemeTrue()
        second = scheme.schemeTrue()
        self.assertIs(first, second, 'schemeTrue is no singleton')
        f = scheme.schemeFalse()
        t = scheme.schemeTrue()
        self.assertNotEqual(t, f, "schemeTrue and schemeFalse should not be equal!")

class TestSchemeNil(TestCase):
    def test_schemeNil(self):
        firstNil = scheme.schemeNil()
        secondNil = scheme.schemeNil()

        self.assertIs(firstNil,secondNil, 'schemeNil should be singleton')

class TestSchemeString(TestCase):
    def test_schemeString(self):
        string = scheme.schemeString('Hello')
        self.assertEqual(string.value,'Hello','schemeString does not work')


class TestSchemeSymbol(TestCase):
    def test_schemeSymbol(self):
        firstSymbol = scheme.schemeSymbol('x')
        secondSymbol = scheme.schemeSymbol('x')
        thirdSymbol = scheme.schemeSymbol('y')
        self.assertEqual(firstSymbol.value, 'x', 'schemeSymbol does not work')
        self.assertIs(firstSymbol, secondSymbol, 'schemeSymbol with same value should be same')
        self.assertIsNot(firstSymbol, thirdSymbol, 'schemeSymbol with different values should not be same')


class TestSchemeNumber(TestCase):
    def test_schemeNumber (self):
        x = scheme.schemeNumber(3)
        y = scheme.schemeNumber(3)

        self.assertEqual(x.value, 3, 'schemeNumber does not work')
        self.assertEqual(x, y, 'equal schemeNumbers are not equal')
        self.assertIs(x, y, 'same schemeNumbers are not same')


class TestSchemeCons(TestCase):
    def test_schemeCons_equal(self):
        first = scheme.schemeCons('hello', 'world')
        second = scheme.schemeCons('1', 2)
        third = scheme.schemeCons('hello', 'world')

        self.assertIsNot(first, second, 'schemeCons should not be singleton')
        self.assertNotEqual(first, second, 'schemeCons function "__eq__" does not work: not equal schemeCons are equal')
        self.assertEqual(first, third, 'schemeCons function "__eq__" does not work: equal schemeCons are not equal')

    def test_schemeCons_car_cdr(self):
        innerCar = scheme.schemeString('Hello')
        innerCdr = scheme.schemeNumber(3)
        outerCar = scheme.schemeNumber(3)

        outerCdr = scheme.schemeCons(innerCar, innerCdr)
        outerCons = scheme.schemeCons(outerCar, outerCdr)

        self.assertEqual(outerCons.car.value, 3, 'schemeCons car does not work')
        self.assertEqual(outerCons.cdr.car.value, 'Hello', 'nested schemeCons do not work')
        self.assertEqual(outerCons.cdr.cdr.value, 3, 'nested schemeCons do not work')
