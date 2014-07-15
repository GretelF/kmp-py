from interpreter.kmp_py import reader, evaluator,scheme,schemeExceptions, initialize
from unittest import TestCase

# initialize global environments and adds initial bindings to globalEnv and syntaxEnv
initialize.initialize()

def eval_string(string, env = evaluator.SchemeEvaluator.globalEnv):
    r = reader.SchemeReader()
    e = evaluator.SchemeEvaluator()
    obj = r.read(scheme.SchemeStringStream(string))
    return e.evaluate(obj, env)

class SchemeEvalSyntax(TestCase):

    def test_eval_if(self):
        obj = eval_string('(if #t 1 "hello")')
        self.assertIsNotNone(obj, 'syntax if should not return None')
        self.assertEqual(obj.type, 'schemeNumber', 'the expression (if #t 1 "hello") should evaluate to schemeNumber 1')
        self.assertEqual(obj.value, 1, 'the expression (if #t 1 "hello") should evaluate to schemeNumber 1')

    def test_eval_if_elsePartIsNotEvaluated(self):
        obj = eval_string('(if #t 1 (aSymbolThatCannotPossiblyHaveABindingAndWillNeverBeEvaluated x y z))')
        self.assertIsNotNone(obj, 'syntax if should not return None')
