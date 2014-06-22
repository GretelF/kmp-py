from interpreter.kmp_py import evaluator,scheme,schemeExceptions
from unittest import TestCase

class SchemeEvaluator(TestCase):
    def test_eval_number(self):
        e = evaluator.SchemeEvaluator()
        obj = e.eval('1')
        self.assertEqual(obj.type, 'schemeNumber', 'A number should evaluate to itself.')
        self.assertEqual(obj.value, 1, 'Evaluated number does not have the right value.')

    def test_eval_string(self):
        e = evaluator.SchemeEvaluator()
        obj = e.eval('"hello"')
        self.assertEqual(obj.type, 'schemeString', 'A string should evaluate to itself.')
        self.assertEqual(obj.value, 'hello', 'Evaluated string does not have the right value.')

    def test_eval_symbol(self):
        e = evaluator.SchemeEvaluator()

        env = scheme.SchemeEnvironment()
        sym1 = scheme.SchemeSymbol('a')
        env.addBinding(sym1, scheme.SchemeNumber(10))

        obj = e.eval('a', env)
        self.assertEqual(obj.type, 'schemeNumber', 'A symbol should evaluate to its binding.')
        self.assertEqual(obj.value, 10, 'The Binding of the symbol a does not have the right value. Should be 10, is {0}'.format(obj.value))

        self.assertRaises(schemeExceptions.NoBindingException, e.eval, 'b', env)