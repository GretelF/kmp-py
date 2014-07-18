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

class SchemeEvaluator(TestCase):
    def test_evaluate_noEnv(self):
        initialize.initialize()
        evaluator.SchemeEvaluator.globalEnv.addBinding(SchemeSymbol('a'), SchemeNumber(3))
        obj = evaluator.SchemeEvaluator().evaluate(SchemeSymbol('a'))
        self.assertEqual(obj.type, 'schemeNumber', 'evaluate should find a in the global environment. a should be bound to schemeNumber')
        self.assertEqual(obj.value, 3, 'a should be bound to 3 in global Environment.')

    def test_eval_noProcedureInList(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '("hello" 1 2)')

    def test_eval_noBindingFound(self):
        self.assertRaises(schemeExceptions.NoBindingException, eval_string, 'noBinding')

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

    def test_eval_string(self):
        obj = eval_string('"hello"')
        self.assertEqual(obj.type, 'schemeString', 'A string should evaluate to itself.')
        self.assertEqual(obj.value, 'hello', 'Evaluated string does not have the right value.')

    def test_eval_true(self):
        obj = eval_string('#t')
        self.assertEqual(obj.type, 'schemeTrue', '#t should evaluate to schemeTrue')

    def test_eval_false(self):
        obj = eval_string('#f')
        self.assertEqual(obj.type, 'schemeFalse', '#f should evaluate to schemeFalse')

    def test_eval_symbol(self):
        initialize.initialize()
        env = SchemeEnvironment()
        sym1 = SchemeSymbol('a')
        env.addBinding(sym1, SchemeNumber(10))
        obj = eval_string('a', env)
        self.assertEqual(obj.type, 'schemeNumber', 'A symbol should evaluate to its binding.')
        self.assertEqual(obj.value, 10, "The Binding of the symbol 'a' does not have the right value. Should be 10, is {0}".format(obj.value))

    def test_eval_symbol_no_binding(self):
        initialize.initialize()
        env = SchemeEnvironment()
        sym1 = SchemeSymbol('a')
        env.addBinding(sym1, SchemeNumber(10))
        self.assertRaises(schemeExceptions.NoBindingException, eval_string, 'b', env)

    def test_eval_eq(self):
        obj = eval_string('(eq? 1 1)')
        self.assertEqual(obj.type, 'schemeTrue', '(eq? 1 1) should evaluate to schemeTrue, but does not.')

        obj = eval_string('(eq? 1 2)')
        self.assertEqual(obj.type, 'schemeFalse', '(eq? 1 2) should evaluate to schemeFalse, but does not.')

    def test_eval_eq_too_many_arguments(self):
        e = evaluator.SchemeEvaluator()
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(eq? 1 2 3)')

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

    def test_eval_minus_noNumber(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(- "hello" "world")')

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

    def test_eval_div_noNumber(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(/ "hello" "world")')

    def test_eval_plus_mul(self):
        obj = eval_string('(+ (* 3 2) 2)')
        self.assertEqual(obj.type, 'schemeNumber', 'Adding and multiplying two numbers should result in another number.')
        self.assertEqual(obj.value, 8, '(+ (* 3 2) 2) should result in 8')

    def test_eval_minus_plus_eq(self):
        obj = eval_string('(eq? (- 6 3) (+ 1 2))')
        self.assertEqual(obj.type, 'schemeTrue', 'A schemeTrue was expected. Got a {0} instead'.format(obj.type))

    def test_eval_no_builtinfunction(self):
        self.assertRaises(schemeExceptions.NoBindingException, eval_string, '(NoBuiltinFunction 2 3)')

    def test_eval_cons(self):
        obj = eval_string('(cons 2 3)')
        self.assertEqual(obj.type, 'schemeCons', 'cons procedure should evaluate to cons')
        self.assertEqual(str(obj), '(2 . 3)', 'expected (2 . 3), got {0}'.format(str(obj)))

    def test_eval_cons_nested(self):
        obj = eval_string('(cons 3 (cons 4 5))')
        self.assertEqual(str(obj), '(3 4 . 5)', 'expected (3 4 . 5), got {0}'.format(str(obj)))

        obj = eval_string('(cons 4 (cons 2 null))')
        self.assertEqual(str(obj), '(4 2)', 'expected (4 2), got {0}'.format(str(obj)))

    def test_eval_cons_eq(self):
        obj = eval_string('(eq? (cons 1 2) (cons 1 2))')
        self.assertEqual(obj.type, 'schemeFalse', 'Two cons should not be same ')

    def test_eval_cons_tooManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(cons 1 2 3)')

    def test_eval_car(self):
        obj = eval_string('(car (cons 1 "hello"))')
        self.assertEqual(obj.type, 'schemeNumber', 'car of cons (1 "hello") should be of type schemeNumber.')
        self.assertEqual(obj.value, 1, 'car of cons (1 "hello") should be 1')

    def test_eval_car_tooManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(car (cons 1 2) (cons 2 3))')

    def test_eval_car_noConsArgument(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(car 1)')

    def test_eval_cdr(self):
        obj = eval_string('(cdr (cons "hello" 2))')
        self.assertEqual(obj.type, 'schemeNumber', 'cdr of cons ("hello" 2) should be of type schemeNumber.')
        self.assertEqual(obj.value, 2, 'car of cons ("hello" 2) should be 2')

    def test_eval_cdr_tooManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(cdr (cons 1 2) (cons 1 2))')

    def test_eval_cdr_noConsArgument(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(cdr 1)')

    def test_eval_print_string_retVal(self):
        obj = eval_string('(print (cons 4 (cons 5 (cons 6 7))))')
        self.assertEqual(obj.type, 'schemeVoid', 'Print procedure should return schemeVoid.')

    def test_eval_print_tooManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(print 1 2 3 4)')

    def test_eval_eq_arithmetic(self):
        obj = eval_string('(= 1 1)')
        self.assertEqual(obj.type, 'schemeTrue', '(= 1 1) should evaluate to schemeTrue')

    def test_eval_eq_arithmetic_toManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string,'(= 1 2 3)')

    def test_eval_eq_arithmetic_noNumberArgument(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(= "hello" "hello")')