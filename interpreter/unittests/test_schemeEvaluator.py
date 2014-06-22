from interpreter.kmp_py import evaluator,scheme,schemeExceptions
from unittest import TestCase

class SchemeEvaluator(TestCase):
    def test_eval_number(self):
        e = evaluator.SchemeEvaluator()
        obj = e.eval_string('1')
        self.assertEqual(obj.type, 'schemeNumber', 'A number should evaluate to itself.')
        self.assertEqual(obj.value, 1, 'Evaluated number does not have the right value.')

    def test_eval_string(self):
        e = evaluator.SchemeEvaluator()
        obj = e.eval_string('"hello"')
        self.assertEqual(obj.type, 'schemeString', 'A string should evaluate to itself.')
        self.assertEqual(obj.value, 'hello', 'Evaluated string does not have the right value.')

    def test_eval_symbol(self):
        e = evaluator.SchemeEvaluator()
        env = scheme.SchemeEnvironment()
        sym1 = scheme.SchemeSymbol('a')
        env.addBinding(sym1, scheme.SchemeNumber(10))
        obj = e.eval_string('a', env)
        self.assertEqual(obj.type, 'schemeNumber', 'A symbol should evaluate to its binding.')
        self.assertEqual(obj.value, 10, "The Binding of the symbol 'a' does not have the right value. Should be 10, is {0}".format(obj.value))

    def test_eval_symbol_no_binding(self):
        e = evaluator.SchemeEvaluator()
        env = scheme.SchemeEnvironment()
        sym1 = scheme.SchemeSymbol('a')
        env.addBinding(sym1, scheme.SchemeNumber(10))
        self.assertRaises(schemeExceptions.NoBindingException, e.eval_string, 'b', env)

    def test_eval_eq(self):
        e = evaluator.SchemeEvaluator()
        obj = e.eval_string('(eq? 1 1)')
        self.assertEqual(obj.type, 'schemeTrue', '(eq? 1 1) should evaluate to schemeTrue, but does not.')

        obj = e.eval_string('(eq? 1 2)')
        self.assertEqual(obj.type, 'schemeFalse', '(eq? 1 2) should evaluate to schemeFalse, but does not.')

    def test_eval_eq_to_many_arguments(self):
        e = evaluator.SchemeEvaluator()
        self.assertRaises(schemeExceptions.InvalidInputException, e.eval_string, '(eq? 1 2 3)')

    def test_eval_plus(self):
        e = evaluator.SchemeEvaluator()
        obj = e.eval_string('(+ 1 2)')
        self.assertEqual(obj.type, 'schemeNumber', 'Adding two numbers should result in another number.')
        self.assertEqual(obj.value, 3, '(+ 1 2) should result in 3')

    def test_eval_minus(self):
        e = evaluator.SchemeEvaluator()
        obj = e.eval_string('(- 44 2)')
        self.assertEqual(obj.type, 'schemeNumber', 'Subtracting two numbers should result in another number.')
        self.assertEqual(obj.value, 42, '(- 44 2) should result in 42')

    def test_eval_mul(self):
        e = evaluator.SchemeEvaluator()
        obj = e.eval_string('(* 10 20)')
        self.assertEqual(obj.type, 'schemeNumber', 'Multiplying two numbers should result in another number.')
        self.assertEqual(obj.value, 200, '(* 10 20) should result in 200')

    def test_eval_div(self):
        e = evaluator.SchemeEvaluator()
        obj = e.eval_string('(/ 20 10)')
        self.assertEqual(obj.type, 'schemeNumber', 'Dividing a number by another should result in another number.')
        self.assertEqual(obj.value, 2, '(/ 20 10) should result in 2')

    def test_eval_plus_mul(self):
        e = evaluator.SchemeEvaluator()
        obj = e.eval_string('(+ (* 3 2) 2)')
        self.assertEqual(obj.type, 'schemeNumber', 'Adding and multiplying two numbers should result in another number.')
        self.assertEqual(obj.value, 8, '(+ (* 3 2) 2) should result in 8')

    def test_eval_no_builtinfunction(self):
        e = evaluator.SchemeEvaluator()
        self.assertRaises(schemeExceptions.NoBindingException, e.eval_string, '(% 2 3)')



