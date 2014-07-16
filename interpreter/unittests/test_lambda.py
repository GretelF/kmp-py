from interpreter.kmp_py import reader, evaluator,schemeExceptions, initialize
from interpreter.kmp_py.scheme import *
from unittest import TestCase

# initialize global environments and adds initial bindings to globalEnv and syntaxEnv
initialize.initialize()

def eval_string(string, env = evaluator.SchemeEvaluator.globalEnv):
    r = reader.SchemeReader()
    e = evaluator.SchemeEvaluator()
    obj = r.read(SchemeStringStream(string))
    return e.evaluate(obj, env)

class test_Lambdas(TestCase):
    def test_lambda_create(self):
        obj = eval_string('(lambda () 1)')
        self.assertIsNotNone(obj, 'syntax lambda should not return None')
        self.assertEqual(obj.type, 'schemeUserDefinedFunction', 'syntax lambda should return a userdefined function.')

    def test_lambda_tooFewArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(lambda x)')
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(lambda)')

    def test_lambda_firstArgumentNoCons(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(lambda 1 2)')




