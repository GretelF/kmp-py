from interpreter.kmp_py import reader, evaluator,schemeExceptions, initialize
from interpreter.kmp_py.scheme import *
from unittest import TestCase

# initialize global environments and adds initial bindings to globalEnv and syntaxEnv
initialize.initialize()

def call_lambda(lambdaObject, args='', env=None):
    if env is None:
        env = evaluator.SchemeEvaluator.globalEnv
    e = evaluator.SchemeEvaluator()
    r = reader.SchemeReader()
    args = r.read(SchemeStringStream('({0})'.format(args)))
    cons = SchemeCons(lambdaObject, args)
    return e.evaluate(cons, env)

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

        obj2 = eval_string('(lambda (a b c) 1 2 3)')
        self.assertEqual(obj2.arglist, [SchemeSymbol('a'), SchemeSymbol('b'), SchemeSymbol('c')], 'lambda should have arglist [a,b,c]')
        self.assertEqual(obj2.bodylist,[SchemeNumber(1), SchemeNumber(2), SchemeNumber(3)], 'lambda should have body [1, 2, 3]' )

    def test_lambda_tooFewArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(lambda x)')
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(lambda)')

    def test_lambda_firstArgumentNoCons(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(lambda 1 2)')

    def test_lambda_name(self):
        eval_string('(define f (lambda () 1))')
        obj = eval_string('f')
        self.assertEqual(obj.name, 'f', 'define did not set the name of the lambda.')
        eval_string('(define g f)')
        obj2 = eval_string('g')
        self.assertEqual(obj2.name, obj.name, 'define should not reset the name of the lambda.')

    def test_lambda_call(self):
        lambdaObject = eval_string('(lambda () 1)')
        obj = call_lambda(lambdaObject)                                                 # call with no arguments
        self.assertEqual(obj.type, 'schemeNumber', 'the lambda should return a type schemeNumber')
        self.assertEqual(obj.value, 1, 'the lambda should return schemeNumber 1')

    def test_lambda_call_returnLambdaArgument(self):
        lambdaObject = eval_string('(lambda (n) n)')
        obj = call_lambda(lambdaObject, '10')                                           # call with argument 10
        self.assertEqual(obj.type, 'schemeNumber', 'the lambda should return the type of the object, that was passed as argument')
        self.assertEqual(obj.value, 10, '10 was passed as argument, so schemeNumber 10 should be returned.')

    def test_lambda_call_tooManyArguments(self):
        lambdaObject = eval_string('(lambda (n) n)')
        self.assertRaises(schemeExceptions.ArgumentCountException, call_lambda, lambdaObject, '10 20 30')

    def test_lambda_call_tooFewArguments(self):
        lambdaObject = eval_string('(lambda (n) n)')
        self.assertRaises(schemeExceptions.ArgumentCountException, call_lambda, lambdaObject)

    def test_lambda_makeAdder(self):
        initialize.initialize()
        eval_string('(define make-adder (lambda(n) (lambda(x) (+ x n))))')
        eval_string('(define add10 (make-adder 10))')
        lambdaObject = eval_string('add10')
        self.assertRaises(schemeExceptions.NoBindingException, eval_string, 'n')            # no global n
        obj = call_lambda(lambdaObject, '5')
        self.assertEqual(obj.type, 'schemeNumber', 'lambda should return type schemeNumber.')
        self.assertEqual(obj.value, 15, 'lambda should return schemeNumber 15.')

    def test_lambda_tak(self):
        initialize.initialize()
        eval_string('(define counter 0)')
        eval_string(''' (define (tak x y z)
                            (set! counter (+ counter 1))
                            (if (< y x)
                                (tak (tak (- x 1)  y z) (tak (- y 1) z x) (tak (- z 1) x y))
                                z
                            )
                        )'''
        )
        obj = eval_string('(tak 4 0 1)')
        self.assertEqual(obj.type, 'schemeNumber', 'tak should return a schemeNumber')
        self.assertEqual(obj.value, 0, 'tak should return schemeNumber 1 for arguments 4 0 1')
        c = eval_string('counter')
        self.assertEqual(c.type, 'schemeNumber', 'counter should be a number.')
        self.assertEqual(c.value, 17, 'the counter should be 17 for tak arguments 4 0 1')









