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

class SchemeEvalSyntax(TestCase):

    def test_eval_if(self):
        obj = eval_string('(if #t 1 "hello")')
        self.assertIsNotNone(obj, 'syntax if should not return None')
        self.assertEqual(obj.type, 'schemeNumber', 'the expression (if #t 1 "hello") should evaluate to type schemeNumber')
        self.assertEqual(obj.value, 1, 'the expression (if #t 1 "hello") should evaluate to schemeNumber 1')

    def test_eval_if_evalElsePart(self):
        obj = eval_string('(if #f 1 "hello")')
        self.assertIsNotNone(obj, 'syntax if should not return None')
        self.assertEqual(obj.type, 'schemeString', 'the expression (if #f 1 "hello") should evaluate to type schemeString')
        self.assertEqual(obj.value, "hello", 'the expression (if #f 1 "hello") should evaluate to schemeString "hello"')

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
        self.assertEqual(eval_string('b'), SchemeNumber(3), 'syntax define does not work. b should be bound to 3 in the global env.')

    def test_eval_define_tooManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string,'(define 1 2 3 4)')

    def test_eval_define_firstArgumentNoSymbol(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string,'(define 1 2)')

    def test_eval_define_noArgument(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string,'(define)')

    def test_eval_define_evaluateSecondArg(self):
        initialize.initialize()
        eval_string('(define a 1)')
        eval_string('(define b a)')
        obj = eval_string('b')
        self.assertEqual(obj.type, 'schemeNumber', 'b should be bound to type schemeNumber')
        self.assertEqual(obj.value, 1, 'b should be bound to schemeNumber 1')

    def test_eval_set(self):
        initialize.initialize()
        eval_string('(define x 3)')
        obj = eval_string('(set! x 42)')
        self.assertIsNotNone(obj, 'syntax set! should not return None.')
        self.assertEqual(obj.type, 'schemeVoid','syntax set! should return schemeVoid.')
        self.assertEqual(eval_string('x'), SchemeNumber(42), 'syntax set! does not work. b should be bound to 42 in the global env.')

    def test_eval_set_noBinding(self):
        initialize.initialize()
        self.assertRaises(schemeExceptions.NoBindingException, eval_string, '(set! c 5)')


    def test_eval_set_tooManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string,'(set! 1 2 3 4)')

    def test_eval_set_firstArgumentNoSymbol(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string,'(set! 1 2)')

    def test_eval_set_noArgument(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string,'(set!)')

    def test_eval_quote(self):
        obj = eval_string('(quote 1)')
        self.assertEqual(obj.type, 'schemeNumber', 'syntax quote should return the unevaluated Argument: schemeNumber 1')
        self.assertEqual(obj.value, 1, 'syntax quote should return schemeNumber 1 for (quote 1)')
        obj = eval_string('(quote a)')
        self.assertEqual(obj.type, 'schemeSymbol', 'syntax quote should return the unevaluated Argument: schemeSymbol a')
        self.assertEqual(obj.value, 'a', 'syntax quote should return schemeSymbol a for (quote a)')

    def test_eval_quote_tooManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(quote 1 2 3)')

    def test_eval_begin(self):
        initialize.initialize()
        obj = eval_string('(begin (define a 1) (define b "hello") 3)')
        self.assertEqual(obj.type, 'schemeNumber', 'syntax begin should evaluate all arguments and return the return value of last one.')
        self.assertEqual(obj.value, 3, 'syntax begin should return the return value of the last evaluated arg')
        obj = eval_string('a')
        self.assertEqual(obj.type, 'schemeNumber', 'after the begin statement, a should be bound to schemeNumber 1')
        self.assertEqual(obj.value, 1, 'after the begin statement, a should be bound to schemeNumber 1')
        obj = eval_string('b')
        self.assertEqual(obj.type, 'schemeString', 'after the begin statement, a should be bound to schemeString "hello"')
        self.assertEqual(obj.value, 'hello', 'after the begin statement, a should be bound to schemeString "hello"')

    def test_eval_and(self):
        initialize.initialize()
        obj = eval_string('(and #t #f)')
        self.assertEqual(obj.type, 'schemeFalse', '(and #t #f) should result in schemeFalse')
        obj = eval_string('(and #t #t)')
        self.assertEqual(obj.type, 'schemeTrue', '(and #t #t) should result in schemeTrue')
        obj = eval_string('(and (= 3 3) (= 4 4))')
        self.assertEqual(obj.type, 'schemeTrue', '(and (= 3 3) (= 4 4)) should result in schemeTrue')

    def test_eval_and_secondArgumentNotEvaluated(self):
        initialize.initialize()
        obj = eval_string('(and #f (aSymbolThatCannotPossiblyHaveABindingAndWillNeverBeEvaluated x y z))')
        self.assertEqual(obj.type, 'schemeFalse', 'If a argument is false the others should not be evaluated.')

    def test_eval_and_noArguments(self):
        obj = eval_string('(and)')
        self.assertEqual(obj.type, 'schemeTrue', '(and) should evaluate to #t')

    def test_eval_or(self):
        initialize.initialize()
        obj = eval_string('(or #t #f)')
        self.assertEqual(obj.type, 'schemeTrue', '(or #t #f) should result in schemeTrue')
        obj = eval_string('(or #f #f)')
        self.assertEqual(obj.type, 'schemeFalse', '(or #f #f) should result in schemeFalse')
        obj = eval_string('(or (= 3 3) (= 4 4))')
        self.assertEqual(obj.type, 'schemeTrue', '(or (= 3 3) (= 4 4)) should result in schemeTrue')

    def test_eval_or_secondArgumentNotEvaluated(self):
        initialize.initialize()
        obj = eval_string('(or #t (aSymbolThatCannotPossiblyHaveABindingAndWillNeverBeEvaluated x y z))')
        self.assertEqual(obj.type, 'schemeTrue', 'If a argument is true the others should not be evaluated.')

    def test_eval_or_noArguments(self):
        obj = eval_string('(or)')
        self.assertEqual(obj.type, 'schemeFalse', '(or) should evaluate to #f')

    def test_eval_lambda(self):
        initialize.initialize()
        eval_string('(define add1 (lambda (n) (+ n 1)))')
        obj = eval_string('add1')
        self.assertEqual(obj.type, 'schemeUserDefinedFunction', 'the lambda shorthand syntax should create a user defined function')
        obj2 = eval_string('(add1 3)')
        self.assertEqual(obj2.type, 'schemeNumber', 'add1 should return a number type')
        self.assertEqual(obj2.value, 4, 'add1 should return 4 if given 3.')

    def test_eval_lambda_moreThanOneBodyElement(self):
        initialize.initialize()
        eval_string('(define f (lambda (n) (define x 1) (+ n x)))')
        obj = eval_string('f')
        self.assertEqual(obj.type, 'schemeUserDefinedFunction', 'the lambda shorthand syntax should create a user defined function')
        obj2 = eval_string('(f 3)')
        self.assertEqual(obj2.type, 'schemeNumber', 'f should return a number type')
        self.assertEqual(obj2.value, 4, 'f should return 4 if given 3.')

    def test_eval_shortHandLambda(self):
        initialize.initialize()
        eval_string('(define (add1 n) (+ n 1))')
        obj = eval_string('add1')
        self.assertEqual(obj.type, 'schemeUserDefinedFunction', 'the lambda shorthand syntax should create a user defined function')
        obj2 = eval_string('(add1 3)')
        self.assertEqual(obj2.type, 'schemeNumber', 'add1 should return a number type')
        self.assertEqual(obj2.value, 4, 'add1 should return 4 if given 3.')

    def test_eval_shortHandLambda_MoreThanOneBodyElement(self):
        initialize.initialize()
        eval_string('(define (f n) (define x 1) (+ n x))')
        obj = eval_string('f')
        self.assertEqual(obj.type, 'schemeUserDefinedFunction', 'the lambda shorthand syntax should create a user defined function')
        obj2 = eval_string('(f 3)')
        self.assertEqual(obj2.type, 'schemeNumber', 'f should return a number type')
        self.assertEqual(obj2.value, 4, 'f should return 4 if given 3.')


