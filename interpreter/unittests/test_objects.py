from unittest import TestCase
from interpreter.kmp_py import initialize, schemeExceptions
from interpreter.kmp_py.scheme import *

# initialize global environments and adds initial bindings to globalEnv and syntaxEnv
initialize.initialize()

class test_SchemeObject(TestCase):
    def test_isTrue(self):
        obj = SchemeObject()
        self.assertTrue(obj.isTrue(), 'schemeObject should return true for isTrue()')

    def test_isFalse(self):
        obj = SchemeObject()
        self.assertFalse(obj.isFalse(), 'schemeObject should return false for isFalse()')

    def test_isNil(self):
        obj = SchemeObject()
        self.assertFalse(obj.isNil(), 'schemeObject should return false for isNil()')

class test_SchemeFalse(TestCase):

    def test_singleton(self):
        first = SchemeFalse()
        second = SchemeFalse()
        self.assertIs(first, second, 'schemeFalse is no singleton.')

    def test_str(self):
        false = SchemeFalse()
        self.assertEqual(str(false), '#f', 'schemeFalse function __str__ does not work.')

    def test_isFalse(self):
        false = SchemeFalse()
        self.assertTrue(false.isFalse(), 'SchemeFalse should return true for isFalse')

    def test_isTrue(self):
        false = SchemeFalse()
        self.assertFalse(false.isTrue(), 'SchemeFalse should return false for isTrue()')

class test_SchemeTrue(TestCase):
    def test_singleton(self):
        first = SchemeTrue()
        second = SchemeTrue()
        self.assertIs(first, second, 'schemeTrue is no singleton.')

    def test_isnotequal_schemeFalse(self):
        f = SchemeFalse()
        t = SchemeTrue()
        self.assertNotEqual(t, f, "schemeTrue and schemeFalse should not be equal!")

    def test_str(self):
        true = SchemeTrue()
        self.assertEqual(str(true), '#t', 'schemeTrue function __str__ does not work.')


class test_SchemeNil(TestCase):
    def test_singleton(self):
        firstNil = SchemeNil()
        secondNil = SchemeNil()
        self.assertIs(firstNil, secondNil, 'schemeNil should be singleton.')

    def test_str(self):
        nil = SchemeNil()
        self.assertEqual(str(nil), '()', 'schemeNil function __str__ does not work.')

    def test_isNil(self):
        nil = SchemeNil()
        self.assertTrue(nil.isNil(), 'SchemeNil should return for isNil()')

class test_SchemeVoid(TestCase):
    def test_singleton(self):
        firstVoid = SchemeVoid()
        secondVoid = SchemeVoid()
        self.assertIs(firstVoid, secondVoid, 'schemeVoid should be singleton.')

    def test_str(self):
        void = SchemeVoid()
        self.assertEqual(str(void), '', 'schemeVoid function __str__ does not work.')

class test_SchemeString(TestCase):
    def test_object(self):
        string = SchemeString('Hello')
        self.assertEqual(string.value, 'Hello', 'schemeString does not work.')

    def test_str(self):
        string = SchemeString('hello')
        self.assertEqual(str(string), '"hello"', 'schemeString function __str__ does not work.')


class test_SchemeSymbol(TestCase):
    def test_object(self):
        firstSymbol = SchemeSymbol('x')
        secondSymbol = SchemeSymbol('y')
        self.assertEqual(firstSymbol.value, 'x', 'schemeSymbol does not work.')
        self.assertIsNot(firstSymbol, secondSymbol, 'schemeSymbol with different values should not be same.')

    def test_sameInstance(self):
        firstSymbol = SchemeSymbol('x')
        secondSymbol = SchemeSymbol('x')
        self.assertIs(firstSymbol, secondSymbol, 'schemeSymbol with same value should be same.')

    def test_str(self):
        symbol = SchemeSymbol('x')
        self.assertEqual(str(symbol), 'x', 'schemeSymbol function __str__ does not work.')


class test_SchemeNumber(TestCase):
    def test_object(self):
        x = SchemeNumber(3)
        y = SchemeNumber(3)

        self.assertEqual(x.value, 3, 'schemeNumber does not work.')
        self.assertEqual(x, y, 'equal schemeNumbers are not equal.')

    def test_negative(self):
        x = SchemeNumber(-1)
        self.assertEqual(x.value, -1, 'schemeNumber does not work for negative numbers')

    def test_sameInstance(self):                                            # TODO: do i really want this???
        x = SchemeNumber(3)
        y = SchemeNumber(3)
        self.assertIs(x, y, 'same schemeNumbers are not same.')

    def test_str(self):
        x = SchemeNumber(3)
        self.assertEqual(str(x), '3', 'schemeNumber function __str__ does not work.')

    def test_float(self):
        x = SchemeNumber(2.4)
        self.assertEqual(x.value, 2.4, 'schemeNumber does not work for floats.')

    def test_float_negative(self):
        x = SchemeNumber(-1.4)
        self.assertEqual(x.value, -1.4, 'schemeNumber does not work for negative floats.')

    def test_float_str(self):
        x = SchemeNumber(2.3)
        self.assertEqual(str(x), '2.3', 'schemeNumber function __str__ does not work for floats.')



class test_SchemeCons(TestCase):
    def test_equal(self):
        first = SchemeCons('hello', 'world')
        second = SchemeCons('1', 2)
        third = SchemeCons('hello', 'world')

        self.assertIsNot(first, second, 'schemeCons should not be singleton.')
        self.assertNotEqual(first, second, 'schemeCons function "__eq__" does not work: schemeCons can only equal itself.')
        self.assertNotEqual(first, third, 'schemeCons function "__eq__" does not work: schemeCons can only equal itself.')

    def test_car_cdr_nested(self):
        innerCar = SchemeString('Hello')
        innerCdr = SchemeNumber(3)
        outerCar = SchemeNumber(5)

        outerCdr = SchemeCons(innerCar, innerCdr)
        outerCons = SchemeCons(outerCar, outerCdr)

        self.assertEqual(outerCons.car.value, 5, 'schemeCons car does not work.')
        self.assertEqual(outerCons.cdr.car.value, 'Hello', 'nested schemeCons do not work.')
        self.assertEqual(outerCons.cdr.cdr.value, 3, 'nested schemeCons do not work.')

    def test_str(self):
        car = SchemeString('hello')
        cdr = SchemeNumber(3)
        cons = SchemeCons(car, cdr)
        self.assertEqual(str(cons), '("hello" . 3)', 'schemeCons function __str__ does not work.')

    def test_str_nested(self):
        innerCar = SchemeString('hello')
        innerCdr = SchemeNumber(10)
        outerCar = SchemeString('aaaaa')

        innerCons = SchemeCons(innerCar, innerCdr)
        outerCons = SchemeCons(outerCar, innerCons)

        self.assertEqual(str(outerCons), '("aaaaa" "hello" . 10)', 'schemeCons function __str__ does not work for nested functions.')

    def test_str_nested_with_nil_as_last_cdr(self):
        innerCar = SchemeNumber(3)
        innerCdr = SchemeNil()
        outerCar = SchemeNumber(5)

        innerCons = SchemeCons(innerCar, innerCdr)
        outerCons = SchemeCons(outerCar, innerCons)

        self.assertEqual(str(outerCons), '(5 3)', 'schemeCons function __str__ does not work for nested functions.')

    def test_str_nested_with_nil_as_car(self):
        innerCar = SchemeNil()
        innerCdr = SchemeNumber(3)
        outerCar = SchemeNumber(5)

        innerCons = SchemeCons(innerCar, innerCdr)
        outerCons = SchemeCons(outerCar, innerCons)

        self.assertEqual(str(outerCons), '(5 () . 3)', 'schemeCons function __str__ does not work for nested functions.')

    def test_str_nested_with_cons_as_car(self):
        innerCar = SchemeNumber(1)
        innerCdr = SchemeNumber(3)
        outerCdr = SchemeNumber(5)

        innerCons = SchemeCons(innerCar, innerCdr)
        outerCons = SchemeCons(innerCons, outerCdr)

        self.assertEqual(str(outerCons), '((1 . 3) . 5)', 'schemeCons function __str__ does not work for nested functions.')

    def test_to_array_regular_list(self):
        one = SchemeNumber(1)
        two = SchemeNumber(2)
        cons = SchemeCons(one, SchemeCons(two, SchemeNil()))
        obj = cons.toArray()

        self.assertEqual(type(obj), list, 'toArray should return a list for regular lists.' )
        self.assertEqual(obj, [one, two], 'toArray should return a list, that represents the cons (1 2) as [1, 2].')

    def test_to_array_irregular_list(self):
        one = SchemeNumber(1)
        three = SchemeNumber(3)
        five = SchemeNumber(5)

        innerCons = SchemeCons(one, three)
        outerCons = SchemeCons(innerCons, five)

        obj = outerCons.toArray()

        self.assertEqual(type(obj), tuple, 'toArray should return a tuple for irregular lists.')
        self.assertEqual(obj, (innerCons, five), 'toArray should return a tuple, that represents the cons ((1 . 3) . 5) as ((cons), 5)')

    def test_is_regular(self):
        one = SchemeNumber(1)
        two = SchemeNumber(2)
        three = SchemeNumber(3)

        cons = SchemeCons(one, SchemeCons(two, three))
        self.assertFalse(cons.isRegular(), '(1 2 . 3) should not be a regular list.')

        cons2 = SchemeCons(one, SchemeCons(two, SchemeNil()))
        self.assertTrue(cons2.isRegular(), '(1 2) should be a regular list.')


class test_SchemeStringStream(TestCase):
    def test_peek(self):
        inString = ('abcde')
        stream = SchemeStringStream(inString)
        self.assertEqual(stream.peek(), 'a', 'schemeStringStream function peek does not work')

    def test_next(self):
        inString = 'ab'
        stream = SchemeStringStream(inString)
        stream.next()
        self.assertEqual(stream.peek(), 'b', 'schemeStringStream function next does not work')
        stream.next()
        self.assertTrue(stream.isAtEndOfStream(), 'cursor should be at end of stream.')
        self.assertEquals(stream.next(),None)

    def test_peek_at_end_of_stream(self):
        inString = 'a'
        stream = SchemeStringStream(inString)
        self.assertEqual(stream.peek(), 'a', 'schemeStringStream faild to peek character')
        stream.next()
        self.assertTrue(stream.isAtEndOfStream(), 'schemeStringStream should be at end of Stream')
        self.assertEqual(stream.peek(), None, 'schemeStringStream should peek None when at end of Stream')

    def test_skipSeparators(self):
        inString1 = '     hello'
        inString2 = '    hello'
        inString3 = '  \t\t\t  hello'
        inString4 = '\n\r\t    hello   world      '
        stream = SchemeStringStream(inString1)
        stream.skipSeparators()
        self.assertEqual(stream.peek(), 'h', 'schemeStringStream function skipSeparators does not work')

        stream = SchemeStringStream(inString2)
        stream.skipSeparators()
        self.assertEqual(stream.peek(), 'h', 'schemeStringStream function skipSeparators does not work')

        stream = SchemeStringStream(inString3)
        stream.skipSeparators()
        self.assertEqual(stream.peek(), 'h', 'schemeStringStream function skipSeparators does not work')

        stream = SchemeStringStream(inString4)
        stream.skipSeparators()
        self.assertEqual(stream.peek(), 'h', 'schemeStringStream function skipSeparators does not work')

    def test_isAtEndofStream(self):
        inString = '       \t    a'
        stream = SchemeStringStream(inString)
        stream.skipSeparators()
        stream.next()
        self.assertTrue(stream.isAtEndOfStream(), 'schemeStringStream function isAtEndOfStream does not work')
        self.assertEquals(stream.next(),None)

    def test_seek(self):
        inString = 'abc'
        stream = SchemeStringStream(inString)
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
        stream = SchemeStringStream(inString)
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


class test_SchemeEnvironment(TestCase):
    def test(self):
        env = SchemeEnvironment()
        sym1 = SchemeSymbol('a')
        sym2 = SchemeSymbol('b')
        env.addBinding(sym1, SchemeNumber(10))
        env.addBinding(sym2, SchemeNumber(20))

        self.assertEqual(env.getBinding(sym1).value, 10, 'schemeEnvironment does not work')
        x = env.getBinding(sym1).value + env.getBinding(sym2).value
        self.assertEqual(x, 30, 'schemeEnvironment does not work')

        sym3 = SchemeSymbol('c')
        env.addBinding(sym3, SchemeString('hello'))
        self.assertEqual(str(env.getBinding(sym3)), '"hello"', 'schemeEnvironment does not work')

        sym4 = SchemeSymbol('d')
        obj4 = SchemeCons(SchemeSymbol('x'), SchemeSymbol('y'))
        env.addBinding(sym4,obj4)
        self.assertEqual(env.getBinding(sym4), obj4, 'schemeEnvironment does not work')

    def test_set_noSymbol(self):
        env = SchemeEnvironment()
        self.assertRaises(schemeExceptions.ArgumentTypeException, env.setBinding, SchemeNumber(4), SchemeString("Hello"))

    def test_add_noSymbol(self):
        env = SchemeEnvironment()
        self.assertRaises(schemeExceptions.ArgumentTypeException, env.addBinding, SchemeString("hello"), SchemeNumber(3))

    def test_parent(self):
        env1 = SchemeEnvironment()
        env2 = SchemeEnvironment(env1)

        sym1 = SchemeSymbol('a')
        sym2 = SchemeSymbol('b')

        obj1 = SchemeNumber(10)
        obj2 = SchemeNumber(20)
        obj3 = SchemeNumber(30)

        env1.addBinding(sym1, obj1)
        env1.addBinding(sym2, obj2)
        env2.addBinding(sym2, obj3)

        self.assertEqual(env2.getBinding(sym1), obj1, 'nested schemeEnvironments do not work')
        self.assertEqual(env1.getBinding(sym2), obj2, 'nested schemeEnvironments do not work')
        self.assertEqual(env2.getBinding(sym2), obj3, 'nested schemeEnvironments do not work')

    def test_identical_symbol(self):
        envParent = SchemeEnvironment()
        envChild = SchemeEnvironment(envParent)

        sym1 = SchemeSymbol('a')         # both should be same instance.
        sym2 = SchemeSymbol('a')

        self.assertIs(sym1, sym2, 'schemeSymbols should be identical, but are not.')

        obj1 = SchemeNumber(10)
        obj2 = SchemeNumber(20)

        envParent.addBinding(sym1, obj1)        # therefore those two Objects should be bind to the same symbol
        envChild.addBinding(sym2, obj2)         # and so envChild can only see obj2 if asked for the binding to sym1,
                                                # even though it was bound to sym2

        self.assertEqual(envChild.getBinding(sym1), obj2, 'nested schemeEnvironments with identical symbols do not work')


class test_SchemeException(TestCase):
    def test_SchemeException(self):
        obj = str(schemeExceptions.SchemeException('This is a SchemeException error message'))
        self.assertEqual(obj, "'This is a SchemeException error message'")








