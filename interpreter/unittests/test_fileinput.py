from interpreter.kmp_py import reader, evaluator,schemeExceptions, initialize
from interpreter.kmp_py.scheme import *
from unittest import TestCase

# initialize global environments and adds initial bindings to globalEnv and syntaxEnv
initialize.initialize()

def eval_string(string, env = None):
    if env is None:
        env = evaluator.SchemeEvaluator.globalEnv
    r = reader.SchemeReader()
    e = evaluator.SchemeEvaluator()
    obj = r.read(SchemeStringStream(string))
    return e.evaluate(obj, env)

class test_FileInput(TestCase):
    def test(self):

        lispCode = ''
        with open('test.lisp', 'r') as f:
            lispCode = "(begin " + f.read() + ")"
        result = eval_string(lispCode)
        f.close()
        self.assertIsNotNone(result, 'result of test.lisp should not be None')
        self.assertEqual(result.type, 'schemeNumber', 'result of test.lisp should be of SchemeNumber type.')
        self.assertEqual(result.value, 1379, 'test.lisp does not return the expected result.')

        x = eval_string("x")
        self.assertEqual(x.value, 42)

        y = eval_string("y")
        self.assertEqual(y.value, 1337)

        add2 = eval_string("add2")
        self.assertEqual(add2.type, 'schemeUserDefinedFunction')
        result = eval_string('(add2 11 13)')
        self.assertEqual(result.value, 24)