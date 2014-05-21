from unittest import TestCase
from interpreter.kmp_py import scheme



class SchemeFalse(TestCase):

    def test_singleton(self):
        first = scheme.SchemeFalse()
        second = scheme.SchemeFalse()
        self.assertIs(first, second, 'schemeFalse is no singleton.')

    def test_str(self):
        false = scheme.SchemeFalse()
        self.assertEqual(str(false), '#f', 'schemeFalse function __str__ does not work.')


class SchemeTrue(TestCase):
    def test_singleton(self):
        first = scheme.SchemeTrue()
        second = scheme.SchemeTrue()
        self.assertIs(first, second, 'schemeTrue is no singleton.')

    def test_isnotequal_schemeFalse(self):
        f = scheme.SchemeFalse()
        t = scheme.SchemeTrue()
        self.assertNotEqual(t, f, "schemeTrue and schemeFalse should not be equal!")

    def test_str(self):
        true = scheme.SchemeTrue()
        self.assertEqual(str(true), '#t', 'schemeTrue function __str__ does not work.')


class SchemeNil(TestCase):
    def test_singleton(self):
        firstNil = scheme.SchemeNil()
        secondNil = scheme.SchemeNil()

        self.assertIs(firstNil, secondNil, 'schemeNil should be singleton.')

    def test_str(self):
        nil = scheme.SchemeNil()
        self.assertEqual(str(nil), '()', 'schemeSymbol function __str__ does not work.')


class SchemeString(TestCase):
    def test_object(self):
        string = scheme.SchemeString('Hello')
        self.assertEqual(string.value, 'Hello', 'schemeString does not work.')

    def test_str(self):
        string = scheme.SchemeString('hello')
        self.assertEqual(str(string), '"hello"', 'schemeString function __str__ does not work.')


class SchemeSymbol(TestCase):
    def test_object(self):
        firstSymbol = scheme.SchemeSymbol('x')
        secondSymbol = scheme.SchemeSymbol('y')
        self.assertEqual(firstSymbol.value, 'x', 'schemeSymbol does not work.')
        self.assertIsNot(firstSymbol, secondSymbol, 'schemeSymbol with different values should not be same.')

    def test_sameInstance(self):
        firstSymbol = scheme.SchemeSymbol('x')
        secondSymbol = scheme.SchemeSymbol('x')
        self.assertIs(firstSymbol, secondSymbol, 'schemeSymbol with same value should be same.')

    def test_str(self):
        symbol = scheme.SchemeSymbol('x')
        self.assertEqual(str(symbol), 'x', 'schemeSymbol function __str__ does not work.')


class SchemeNumber(TestCase):
    def test_object(self):
        x = scheme.SchemeNumber(3)
        y = scheme.SchemeNumber(3)

        self.assertEqual(x.value, 3, 'schemeNumber does not work.')
        self.assertEqual(x, y, 'equal schemeNumbers are not equal.')

    def test_negative(self):
        x = scheme.SchemeNumber(-1)
        self.assertEqual(x.value, -1, 'schemeNumber does not work for negative numbers')

    def test_sameInstance(self):                                            # TODO: do i really want this???
        x = scheme.SchemeNumber(3)
        y = scheme.SchemeNumber(3)
        self.assertIs(x, y, 'same schemeNumbers are not same.')

    def test_str(self):
        x = scheme.SchemeNumber(3)
        self.assertEqual(str(x), '3', 'schemeNumber function __str__ does not work.')


class SchemeCons(TestCase):
    def test_equal(self):
        first = scheme.SchemeCons('hello', 'world')
        second = scheme.SchemeCons('1', 2)
        third = scheme.SchemeCons('hello', 'world')

        self.assertIsNot(first, second, 'schemeCons should not be singleton.')
        self.assertNotEqual(first, second, 'schemeCons function "__eq__" does not work: not equal schemeCons are equal.')
        self.assertEqual(first, third, 'schemeCons function "__eq__" does not work: equal schemeCons are not equal.')

    def test_car_cdr_nested(self):
        innerCar = scheme.SchemeString('Hello')
        innerCdr = scheme.SchemeNumber(3)
        outerCar = scheme.SchemeNumber(5)

        outerCdr = scheme.SchemeCons(innerCar, innerCdr)
        outerCons = scheme.SchemeCons(outerCar, outerCdr)

        self.assertEqual(outerCons.car.value, 5, 'schemeCons car does not work.')
        self.assertEqual(outerCons.cdr.car.value, 'Hello', 'nested schemeCons do not work.')
        self.assertEqual(outerCons.cdr.cdr.value, 3, 'nested schemeCons do not work.')

    def test_str(self):
        car = scheme.SchemeString('hello')
        cdr = scheme.SchemeNumber(3)
        cons = scheme.SchemeCons(car, cdr)
        self.assertEqual(str(cons), '("hello" . 3)', 'schemeCons function __str__ does not work.')

    def test_str_nested(self):
        innerCar = scheme.SchemeString('hello')
        innerCdr = scheme.SchemeNumber(10)
        outerCar = scheme.SchemeString('aaaaa')

        innerCons = scheme.SchemeCons(innerCar, innerCdr)
        outerCons = scheme.SchemeCons(outerCar, innerCons)

        self.assertEqual(str(outerCons), '("aaaaa" "hello" . 10)', 'schemeCons function __str__ does not work for nested functions.')

    def test_str_nested_with_nil_as_last_cdr(self):
        innerCar = scheme.SchemeNumber(3)
        innerCdr = scheme.SchemeNil()
        outerCar = scheme.SchemeNumber(5)

        innerCons = scheme.SchemeCons(innerCar, innerCdr)
        outerCons = scheme.SchemeCons(outerCar, innerCons)

        self.assertEqual(str(outerCons), '(5 3)', 'schemeCons function __str__ does not work for nested functions.')

    def test_str_nested_with_nil_as_car(self):
        innerCar = scheme.SchemeNil()
        innerCdr = scheme.SchemeNumber(3)
        outerCar = scheme.SchemeNumber(5)

        innerCons = scheme.SchemeCons(innerCar, innerCdr)
        outerCons = scheme.SchemeCons(outerCar, innerCons)

        self.assertEqual(str(outerCons), '(5 () . 3)', 'schemeCons function __str__ does not work for nested functions.')

    def test_str_nested_with_cons_as_car(self):
        innerCar = scheme.SchemeNumber(1)
        innerCdr = scheme.SchemeNumber(3)
        outerCdr = scheme.SchemeNumber(5)

        innerCons = scheme.SchemeCons(innerCar, innerCdr)
        outerCons = scheme.SchemeCons(innerCons, outerCdr)

        self.assertEqual(str(outerCons), '((1 . 3) . 5)', 'schemeCons function __str__ does not work for nested functions.')


class SchemeStringStream(TestCase):
    def test_peek(self):
        inString = ('abcde')
        stream = scheme.SchemeStringStream(inString)
        self.assertEqual(stream.peek(), 'a', 'schemeStringStream function peek does not work')

    def test_next(self):
        inString = 'ab'
        stream = scheme.SchemeStringStream(inString)
        stream.next()
        self.assertEqual(stream.peek(), 'b', 'schemeStringStream function next does not work')
        stream.next()
        self.assertTrue(stream.isAtEndOfStream(), 'cursor should be at end of stream.')
        self.assertEquals(stream.next(),None)

    def test_skipSeparators(self):
        inString1 = '     hello'
        inString2 = '    hello'
        inString3 = '  \t\t\t  hello'
        inString4 = '\n\r\t    hello   world      '
        stream = scheme.SchemeStringStream(inString1)
        stream.skipSeparators()
        self.assertEqual(stream.peek(), 'h', 'schemeStringStream function skipSeparators does not work')

        stream = scheme.SchemeStringStream(inString2)
        stream.skipSeparators()
        self.assertEqual(stream.peek(), 'h', 'schemeStringStream function skipSeparators does not work')

        stream = scheme.SchemeStringStream(inString3)
        stream.skipSeparators()
        self.assertEqual(stream.peek(), 'h', 'schemeStringStream function skipSeparators does not work')

        stream = scheme.SchemeStringStream(inString4)
        stream.skipSeparators()
        self.assertEqual(stream.peek(), 'h', 'schemeStringStream function skipSeparators does not work')

    def test_isAtEndofStream(self):
        inString = '       \t    a'
        stream = scheme.SchemeStringStream(inString)
        stream.skipSeparators()
        stream.next()
        self.assertTrue(stream.isAtEndOfStream(), 'schemeStringStream function isAtEndOfStream does not work')
        self.assertEquals(stream.next(),None)

    def test_seek(self):
        inString = 'abc'
        stream = scheme.SchemeStringStream(inString)
        stream.seek(2)
        self.assertEqual(stream.peek(), 'c', 'schemeStringStream function seek does not work')
        stream.seek(-2)
        self.assertEqual(stream.peek(), 'b', 'schemeStringStream function seek does not work')
        stream.next()
        self.assertEqual(stream.peek(), 'c', 'schemeStringStream function seek does not work')
        stream.next()
        self.assertTrue(stream.isAtEndOfStream(), 'cursor should be at end of stream')
        stream.seek(-3)
        self.assertEqual(stream.peek(), 'a', 'schemeStringStream function seek does not work')

        #test if seek parameters are clamped to length of inString
        stream.seek(7)
        self.assertEqual(stream.peek(), 'c', 'schemeStringStream function seek does not work')
        stream.seek(-5)
        self.assertEqual(stream.peek(), 'a', 'schemeStringStream function seek does not work')

    def test_whole(self):
        inString = '  \t hello     world \n\n xxx'
        stream = scheme.SchemeStringStream(inString)
        self.assertEqual(stream.peek(), ' ', 'schemeStringStream function peek does not work')
        stream.next()
        self.assertEqual(stream.peek(), ' ', 'schemeStringStream function next does not work')
        stream.skipSeparators()
        self.assertEqual(stream.peek(), 'h', 'schemeStringStream function skipSeparators does not work')
        while(stream.peek() != ' '):
            stream.next()
        self.assertEqual(stream.peek(), ' ', 'schemeStringStream function next does not work')
        stream.skipSeparators()
        self.assertEqual(stream.peek(), 'w', 'schemeStringStream function skipSeparators does not work')
        while(stream.peek() != ' '):
            stream.next()
        stream.skipSeparators()
        self.assertEqual(stream.peek(), 'x', 'schemeStringStream function skipSeparators does not work')
        stream.seek(-12)
        self.assertEqual(stream.peek(), 'w', 'schemeStringStream function seek does not work')
        stream.next()
        self.assertEqual(stream.peek(), 'o', 'schemeStringStream function next does not work')


class SchemeEnvironment(TestCase):
    def test(self):
        env = scheme.SchemeEnvironment()
        sym1 = scheme.SchemeSymbol('a')
        sym2 = scheme.SchemeSymbol('b')
        env.addBinding(sym1, scheme.SchemeNumber(10))
        env.addBinding(sym2, scheme.SchemeNumber(20))

        self.assertEqual(env.getBinding(sym1).value, 10, 'schemeEnvironment does not work')
        x = env.getBinding(sym1).value + env.getBinding(sym2).value
        self.assertEqual(x, 30, 'schemeEnvironment does not work')

        sym3 = scheme.SchemeSymbol('c')
        env.addBinding(sym3, scheme.SchemeString('hello'))
        self.assertEqual(str(env.getBinding(sym3)), '"hello"', 'schemeEnvironment does not work')

        sym4 = scheme.SchemeSymbol('d')
        obj4 = scheme.SchemeCons(scheme.SchemeSymbol('x'), scheme.SchemeSymbol('y'))
        env.addBinding(sym4,obj4)
        self.assertEqual(env.getBinding(sym4), obj4, 'schemeEnvironment does not work')

    def test_parent(self):
        env1 = scheme.SchemeEnvironment()
        env2 = scheme.SchemeEnvironment(env1)

        sym1 = scheme.SchemeSymbol('a')
        sym2 = scheme.SchemeSymbol('b')

        obj1 = scheme.SchemeNumber(10)
        obj2 = scheme.SchemeNumber(20)
        obj3 = scheme.SchemeNumber(30)

        env1.addBinding(sym1, obj1)
        env1.addBinding(sym2, obj2)
        env2.addBinding(sym2, obj3)

        self.assertEqual(env2.getBinding(sym1), obj1, 'nested schemeEnvironments do not work')
        self.assertEqual(env1.getBinding(sym2), obj2, 'nested schemeEnvironments do not work')
        self.assertEqual(env2.getBinding(sym2), obj3, 'nested schemeEnvironments do not work')

    def test_identical_symbol(self):
        envParent = scheme.SchemeEnvironment()
        envChild = scheme.SchemeEnvironment(envParent)

        sym1 = scheme.SchemeSymbol('a')         # both should be same instance.
        sym2 = scheme.SchemeSymbol('a')

        obj1 = scheme.SchemeNumber(10)
        obj2 = scheme.SchemeNumber(20)

        envParent.addBinding(sym1, obj1)        # therefore those two Objects should be bind to the same symbol
        envChild.addBinding(sym2, obj2)         # and so envChild can only see obj2 if asked for the binding to sym1,
                                                # even though it was bound to sym2

        self.assertEqual(envChild.getBinding(sym1), obj2, 'nested schemeEnvironments with identical symbols do not work')







