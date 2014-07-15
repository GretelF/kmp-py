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

    def test_eval_if_tooManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string,'(if 1 2 3 4)')

    def test_eval_if_noArgument(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string,'(if)')


    def test_eval_define(self):
        initialize.initialize()
        self.assertRaises(schemeExceptions.NoBindingException, eval_string, 'b')    # with global env.
        obj = eval_string('(define b 3)')
        self.assertIsNotNone(obj, 'syntax define should not return None.')
        self.assertEqual(obj.type, 'schemeVoid','syntax define should return schemeVoid.')
        self.assertEqual(eval_string('b'), scheme.SchemeNumber(3), 'syntax define does not work. b should be bound to 3 in the global env.')

    def test_eval_define_tooManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string,'(define 1 2 3 4)')

    def test_eval_define_firstArgumentNoSymbol(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string,'(define 1 2)')

    def test_eval_define_noArgument(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string,'(define)')


    def test_eval_set(self):
        initialize.initialize()
        eval_string('(define x 3)')
        obj = eval_string('(set! x 42)')
        self.assertIsNotNone(obj, 'syntax set! should not return None.')
        self.assertEqual(obj.type, 'schemeVoid','syntax set! should return schemeVoid.')
        self.assertEqual(eval_string('x'), scheme.SchemeNumber(42), 'syntax set! does not work. b should be bound to 42 in the global env.')

    def test_eval_set_noBinding(self):
        initialize.initialize()
        self.assertRaises(schemeExceptions.NoBindingException, eval_string, '(set! c 5)')


    def test_eval_set_tooManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string,'(set! 1 2 3 4)')

    def test_eval_set_firstArgumentNoSymbol(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string,'(set! 1 2)')

    def test_eval_set_noArgument(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string,'(set!)')