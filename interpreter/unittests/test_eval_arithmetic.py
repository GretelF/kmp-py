from interpreter.kmp_py import reader, evaluator,schemeExceptions, initialize
from interpreter.kmp_py.scheme import *
from unittest import TestCase
import sys

# initialize global environments and adds initial bindings to globalEnv and syntaxEnv
initialize.initialize()

def eval_string(string, env = evaluator.SchemeEvaluator.globalEnv):
    r = reader.SchemeReader()
    e = evaluator.SchemeEvaluator()
    obj = r.read(SchemeStringStream(string))
    return e.evaluate(obj, env)

class SchemeEvaluatorArithmetic(TestCase):

    def test_eval_number(self):
        obj = eval_string('1')
        self.assertEqual(obj.type, 'schemeNumber', 'A number should evaluate to itself.')
        self.assertEqual(obj.value, 1, 'Evaluated number does not have the right value.')

    def test_eval_number_negative(self):
        obj = eval_string('-3')
        self.assertEqual(obj.type, 'schemeNumber', 'A number should evaluate to itself.')
        self.assertEqual(obj.value, -3, 'Evaluated number does not have the right value.')

    def test_eval_float(self):
        obj = eval_string('3.14')
        self.assertEqual(obj.type, 'schemeNumber', 'A number should evaluate to itself.')
        self.assertEqual(obj.value, 3.14, 'Evaluated number does not have the right value.')

    def test_eval_float_negative(self):
        obj = eval_string('-3.14')
        self.assertEqual(obj.type, 'schemeNumber', 'A number should evaluate to itself.')
        self.assertEqual(obj.value, -3.14, 'Evaluated number does not have the right value.')

    def test_eval_plus(self):
        obj = eval_string('(+ 1 2)')
        self.assertEqual(obj.type, 'schemeNumber', 'Adding two numbers should result in another number.')
        self.assertEqual(obj.value, 3, '(+ 1 2) should result in 3')

    def test_eval_plus_with_negative(self):
        obj = eval_string('(+ -3 5)')
        self.assertEqual(obj.type, 'schemeNumber', 'Adding two numbers should result in another number.')
        self.assertEqual(obj.value, 2, '(+ -3 5) should result in 2')

    def test_eval_plus_noNumber(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(+ "hello" "world")')

    def teest_eval_plus_float(self):
        obj = eval_string('(+ 3.4 3)')
        self.assertEqual(obj.type, 'schemeNumber', 'Adding two numbers should result in another number, even if one is float.')
        self.assertEqual(obj.value, 6.4, '(+ 3.4 3) should result in 6.4')

    def teest_eval_plus_two_float(self):
        obj = eval_string('(+ 3.4 1.2)')
        self.assertEqual(obj.type, 'schemeNumber', 'Adding two floats should result in schemeNumber.')
        self.assertEqual(obj.value, 4.6, '(+ 3.4 1.2) should result in 4.6')

    def test_eval_minus(self):
        obj = eval_string('(- 44 2)')
        self.assertEqual(obj.type, 'schemeNumber', 'Subtracting two numbers should result in another number.')
        self.assertEqual(obj.value, 42, '(- 44 2) should result in 42')

    def test_eval_minus_with_negative_result(self):
        obj = eval_string('(- 10 20)')
        self.assertEqual(obj.type, 'schemeNumber', 'Subtracting two numbers should result in another number.')
        self. assertEqual(obj.value, -10, '(- 10 20) should result in -10')

    def test_eval_minus_oneArgument(self):
        obj = eval_string('(- 3)')
        self.assertEqual(obj.type, 'schemeNumber', 'Subtracting should result in a number.')
        self.assertEqual(obj.value, -3, '(- 3) should result in -3')

    def test_eval_minus_noNumber(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(- "hello" "world")')

    def test_eval_minus_tooFewArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(-)')

    def test_eval_mul(self):
        obj = eval_string('(* 10 20)')
        self.assertEqual(obj.type, 'schemeNumber', 'Multiplying two numbers should result in another number.')
        self.assertEqual(obj.value, 200, '(* 10 20) should result in 200')

    def test_eval_mul_noNumber(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(* "hello" "world")')

    def test_eval_div(self):
        obj = eval_string('(/ 20 10)')
        self.assertEqual(obj.type, 'schemeNumber', 'Dividing a number by another should result in another number.')
        self.assertEqual(obj.value, 2, '(/ 20 10) should result in 2')

    def test_eval_div_divisionByZero(self):
        self.assertRaises(schemeExceptions.DivisionByZero, eval_string, '(/ 3 0)')

    def test_eval_div_noNumber(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(/ "hello" 3)')

    def test_eval_div_oneArgument(self):
        obj = eval_string('(/ 4)')
        self.assertEqual(obj.type, 'schemeNumber', 'Division should result in a number.')
        self.assertEqual(obj.value, 0.25, '(/ 4) should result in 1/4, i. e. in 0.25.')

    def test_eval_div_oneArgument_Zero(self):
        self.assertRaises(schemeExceptions.DivisionByZero, eval_string, '(/ 0)')

    def test_eval_div_tooFewArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(/)')

    def test_eval_modulo(self):
        obj = eval_string('(% 20 10)')
        self.assertEqual(obj.type, 'schemeNumber', 'Dividing a number by another should result in another number.')
        self.assertEqual(obj.value, 0, '(% 20 10) should result in 0')
        obj = eval_string('(% 7 4)')
        self.assertEqual(obj.type, 'schemeNumber', 'Dividing a number by another should result in another number.')
        self.assertEqual(obj.value, 3, '(% 7 4) should result in 3')
        obj = eval_string('(% 4 7)')
        self.assertEqual(obj.type, 'schemeNumber', 'Dividing a number by another should result in another number.')
        self.assertEqual(obj.value, 4, '(% 4 7) should result in 4')
        obj = eval_string('(% 0 7)')
        self.assertEqual(obj.type, 'schemeNumber', 'Dividing a number by another should result in another number.')
        self.assertEqual(obj.value, 0, '(% 0 7) should result in 0')

    def test_eval_modulo_noNumber(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(% "hello" 3)')
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(% 3 "hello")')

    def test_eval_modulo_ZeroArgument(self):
        self.assertRaises(schemeExceptions.DivisionByZero, eval_string, '(% 2 0)')

    def test_eval_modulo_tooManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(% 3 4 5)')

    def test_eval_modulo_tooFewArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(% 10)')

    def test_eval_gt(self):
        obj = eval_string('(> 20 10)')
        self.assertEqual(obj.type, 'schemeTrue', '20 is greater than 10, so (> 20 10) should result in schemeTrue.')

        obj = eval_string('(> 10 20)')
        self.assertEqual(obj.type, 'schemeFalse', '10 is not greater than 20, so (> 10 20) should result in schemeFalse.')

        obj = eval_string('(>= 20 10)')
        self.assertEqual(obj.type, 'schemeTrue', '20 is greater than 10, so (>= 20 10) should result in schemeTrue.')

        obj = eval_string('(>= 10 20)')
        self.assertEqual(obj.type, 'schemeFalse', '10 is greater than 20, so (>= 10 20) should result in schemeFalse.')

        obj = eval_string('(>= 20 20)')
        self.assertEqual(obj.type, 'schemeTrue', '20 equal to 20, so (>= 20 20) should result in schemeTrue.')

    def test_eval_gt_tooManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(> 10 20 30)')
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(>= 10 20 30)')

    def test_eval_gt_tooFewArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(> 10)')
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(>= 10)')

    def test_eval_lt(self):
        obj = eval_string('(< 20 10)')
        self.assertEqual(obj.type, 'schemeFalse', '20 is not greater than 10, so (< 20 10) should result in schemeFalse.')

        obj = eval_string('(< 10 20)')
        self.assertEqual(obj.type, 'schemeTrue', '10 is not greater than 20, so (< 10 20) should result in schemeTrue.')

        obj = eval_string('(<= 20 10)')
        self.assertEqual(obj.type, 'schemeFalse', '20 is greater than 10, so (<= 20 10) should result in schemeFalse.')

        obj = eval_string('(<= 10 20)')
        self.assertEqual(obj.type, 'schemeTrue', '10 is greater than 20, so (<= 10 20) should result in schemeTrue.')

        obj = eval_string('(<= 20 20)')
        self.assertEqual(obj.type, 'schemeTrue', '20 equal to 20, so (<= 20 20) should result in schemeTrue.')

    def test_eval_lt_tooManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(< 10 20 30)')
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(<= 10 20 30)')

    def test_eval_lt_tooFewArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(< 10)')
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(<= 10)')


    def test_eval_plus_mul(self):
        obj = eval_string('(+ (* 3 2) 2)')
        self.assertEqual(obj.type, 'schemeNumber', 'Adding and multiplying two numbers should result in another number.')
        self.assertEqual(obj.value, 8, '(+ (* 3 2) 2) should result in 8')

    def test_eval_minus_plus_eq(self):
        obj = eval_string('(eq? (- 6 3) (+ 1 2))')
        self.assertEqual(obj.type, 'schemeTrue', 'A schemeTrue was expected. Got a {0} instead'.format(obj.type))

    def test_eval_abs(self):
        obj = eval_string('(abs 5)')
        self.assertEqual(obj.type, 'schemeNumber', '(abs 5) should evaluate to type schemeNumber.')
        self.assertEqual(obj.value, 5, '(abs 5) should evaluate to schemeNumber 5.')
        obj = eval_string('(abs -5)')
        self.assertEqual(obj.type, 'schemeNumber', '(abs -5) should evaluate to type schemeNumber.')
        self.assertEqual(obj.value, 5, '(abs 5) should evaluate to schemeNumber 5.')
        obj = eval_string('(abs 0)')
        self.assertEqual(obj.type, 'schemeNumber', '(abs 0) should evaluate to type schemeNumber.')
        self.assertEqual(obj.value, 0, '(abs 0) should evaluate to schemeNumber 0.')

    def test_eval_abs_tooManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(abs 1 2 3)')

    def test_eval_abs_tooFewArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(abs)')

    def test_eval_abs_noNumber(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(abs "hello")')

    def test_eval_eq_arithmetic(self):
        obj = eval_string('(= 1 1)')
        self.assertEqual(obj.type, 'schemeTrue', '(= 1 1) should evaluate to schemeTrue')

    def test_eval_eq_arithmetic_toManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string,'(= 1 2 3)')

    def test_eval_eq_arithmetic_noNumberArgument(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(= "hello" "hello")')