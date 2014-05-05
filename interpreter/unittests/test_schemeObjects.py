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

class TestSchemeCons(TestCase):
    def test_schemeCons_equal(self):
        first = scheme.schemeCons('hello','world')
        second = scheme.schemeCons('1',2)
        third = scheme.schemeCons('hello','world')

        self.assertIsNot(first,second,'schemeCons should not be singleton')
        self.assertNotEqual(first,second,'schemeCons function "__eq__" does not work: not equal schemeCons are equal')
        self.assertEqual(first,third,'schemeCons function "__eq__" does not work: equal schemeCons are not equal')

    def test_schemeCons_car(self):
        firstString = scheme.schemeString('Hello')
        secondString = scheme.schemeString('World')

        firstCons = scheme.schemeCons(firstString,secondString)

        self.assertEqual(firstCons.car.value,'Hello','schemeCons car does not work')
