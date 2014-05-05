from unittest import TestCase
from interpreter.kmp_py import scheme

__author__ = 'maria'


class TestSchemeFalse(TestCase):

    def test_schemeFalse(self):
        first = scheme.schemeFalse()
        second = scheme.schemeFalse()
        self.assertIs(first,second,'schemeFalse is no singleton')

class TestSchemeTrue(TestCase):
     def test_schemeTrue(self):
        first = scheme.schemeTrue()
        second = scheme.schemeTrue()
        self.assertIs(first,second,'schemeTrue is no singleton')

class TestSchemeString(TestCase):
    def test_schemeString(self):
        string = scheme.schemeString('Hello')
        self.assertEqual(string.value,'Hello','schemeString does not work')

class TestSchemeInteger(TestCase):
    def test_schemeInteger (self):
        x = scheme.schemeInteger(3)
        y = scheme.schemeInteger(3)
        self.assertEqual(x.value,3,'schemeInteger does not work')
        self.assertEqual(x,y,'equal schemeIntegers are not equal')
#       self.assertIs(x,y,'same schemeIntegers are not same')


class TestSchemeCons(TestCase):
    def test_schemeCons_equal(self):
        first = scheme.schemeCons('hello','world')
        second = scheme.schemeCons('1',2)
        third = scheme.schemeCons('hello','world')

        self.assertIsNot(first,second,'schemeCons should not be singleton')
        self.assertNotEqual(first,second,'schemeCons function "__eq__" does not work: not equal schemeCons are equal')
        self.assertEqual(first,third,'schemeCons function "__eq__" does not work: equal schemeCons are not equal')

    def test_schemeCons_car_cdr(self):
        innerCar = scheme.schemeString('Hello')
        innerCdr = scheme.schemeInteger(3)
        outerCar = scheme.schemeInteger(3)

        outerCdr = scheme.schemeCons(innerCar,innerCdr)
        outerCons = scheme.schemeCons(outerCar,outerCdr)

        self.assertEqual(outerCons.car.value,3,'schemeCons car does not work')
        self.assertEqual(outerCons.cdr.car.value,'Hello','nested schemeCons do not work')
        self.assertEqual(outerCons.cdr.cdr.value,3,'nested schemeCons do not work')
