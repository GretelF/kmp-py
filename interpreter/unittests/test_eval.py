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
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(eq? 1 2 3)')

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

    def test_eval_list(self):
        obj = eval_string("(list 1 2 3 4)")
        self.assertEqual(obj.type, 'schemeCons', 'builtin function list should return a schemeCons type or SchemeNil')
        self.assertEqual(str(obj), '(1 2 3 4)', 'builtin function list does not work correctly.')

    def test_eval_list_empty(self):
        obj = eval_string('(list)')
        self.assertEqual(obj.type, 'schemeNil', 'builtin function list should return a schemeNil, if called without arguments.')

    def test_eval_print_tooManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(print 1 2 3 4)')

    def test_eval_recursion_limit_get(self):
        obj = eval_string('(recursion-limit)')
        self.assertEqual(obj.type, 'schemeNumber', 'recursion-limit without argument should return type schemeNumber')
        self.assertEqual(obj.value, sys.getrecursionlimit(), 'recursion-limit does not return the systems recursion limit')

    def test_eval_recursion_limit_set(self):
        obj = eval_string('(recursion-limit 2000)')
        self.assertEqual(obj.type, 'schemeVoid', 'recursion-limit with argument should return type schemeVoid')
        self.assertEqual(sys.getrecursionlimit(), 2000, 'recursion-limit does not set systems recursion limit')

    def test_eval_recursion_limit_tooManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(recursion-limit 1000 2000 3000)')

    def test_eval_recursion_limit_wrongArgumentType(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(recursion-limit "hello")')

    def test_eval_type(self):
        obj = eval_string('(type? 2)')
        self.assertEqual(obj.value, 'schemeNumber', 'The type of 2 should be schemeNumber.')
        obj = eval_string('(type? (define x 2))')
        self.assertEqual(obj.value, 'schemeVoid', 'The return value of (define x 2) should be schemeVoid.')

    def test_eval_type_tooManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(type? 1 2 3)')

    def test_eval_isList(self):
        obj = eval_string('(list? (list 1 2))')
        self.assertEqual(obj.type, 'schemeTrue', 'list? should return SchemeTrue for (1 2)')
        obj2 = eval_string('(list? (cons 1 2))')
        self.assertEqual(obj2.type, 'schemeFalse', 'list? should return SchemeFalse for (1 . 2)')

    def test_eval_isList_toManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(list? 1 2 3)')

    def test_eval_isList_noConsArgument(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(list? 1)')

    def test_eval_isList_SchemeNil(self):
        obj = eval_string('(list? nil)')
        self.assertEqual(obj.type, 'schemeTrue', 'list? should return SchemeTrue for SchemeNil.')



    def test_eval_not(self):
        obj = eval_string('(not #t)')
        self.assertEqual(obj.type, 'schemeFalse', '(not #t) should return schemeFalse.')
        obj = eval_string('(not (if (= (+ 1 2) (- 4 1)) #f #t))')
        self.assertEqual(obj.type, 'schemeTrue', 'Expected schemeTrue, but got schemeFalse.')
        obj = eval_string('(not 3)')
        self.assertEqual(obj.type, 'schemeFalse', '(not 3) should return schemeFalse')
        obj = eval_string('(not #f)')
        self.assertEqual(obj.type, 'schemeTrue', '(not #f) should return schemeTrue')

    def test_eval_not_tooManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(not #t #f)')

    def test_eval_map(self):
        initialize.initialize()
        eval_string('(define plus1 (lambda (n) (+ n 1)))')
        obj = eval_string('(map plus1 (list 1 2 3 4))')
        self.assertEqual(obj.type, 'schemeCons', 'function map should return a list')
        self.assertEqual(str(obj), '(2 3 4 5)', 'function map should apply plus1 to each given list element.')

    def test_eval_map_tooFewArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(map plus1)')

    def test_eval_map_functionCall_tooFewArguments(self):
        initialize.initialize()
        eval_string('(define addElementWise (lambda (n m) (+ n m)))')
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(map addElementWise (list 1 2 3))')

    def test_eval_map_functionCall_tooManyArguments(self):
        initialize.initialize()
        eval_string('(define addElementWise (lambda (n m) (+ n m)))')
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(map addElementWise (list 1 2 3) (list 2 3 4) (list 3 4 5))')

    def test_eval_map_listsNotSameSize(self):
        initialize.initialize()
        eval_string('(define addElementWise (lambda (n m) (+ n m)))')
        self.assertRaises(schemeExceptions.InvalidInputException, eval_string, '(map addElementWise (list 1 2 3 4) (list 2 3 4))')

    def test_eval_map_notCallable(self):
        initialize.initialize()
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(map 3 (list 2 3 4))')

    def test_eval_map_noLists(self):
        initialize.initialize()
        eval_string('(define addElementWise (lambda (n m) (+ n m)))')
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(map addElementWise 3 4)')
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(map addElementWise (list 1 2) 4)')
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(map addElementWise 3 (list 1 2))')

    def test_eval_map_nils(self):
        initialize.initialize()
        eval_string('(define addElementWise (lambda (n m) (+ n m)))')
        obj = eval_string('(map addElementWise () ())')
        self.assertEqual(obj.type, 'schemeNil', 'map should return schemeNil if applied to empty lists.')

    def test_eval_setBindingInOuterEnv(self):
        initialize.initialize()
        eval_string('(define x 1)')
        eval_string('(define f (lambda (z) (set! x z)))')
        eval_string('(f 3)')
        obj = eval_string('x')
        self.assertEqual(obj.type, 'schemeNumber', 'x should be bound to a schemeNumber type.')
        self.assertEqual(obj.value, 3, 'after f is called, x should be bound to 3.')

    def test_eval_first(self):
        obj = eval_string('(first (list 1 2 3))')
        self.assertIsNotNone(obj, 'first should not return None.')
        self.assertEqual(obj.type, 'schemeNumber', 'first should return the first element of the list, which is in this case a number.')
        self.assertEqual(obj.value, 1, 'the number first should return should be 1')

    def test_eval_first_tooManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(first (list 1 2 3) (list 2 3 4))')

    def test_eval_first_tooFewArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(first)')

    def test_eval_first_noListArgument(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(first 1)')

    def test_eval_first_emptyListArgument(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(first (list))')

    def test_eval_rest(self):
        obj = eval_string('(rest (list 1 2 3))')
        self.assertIsNotNone(obj, 'rest should not return None.')
        self.assertEqual(obj.type, 'schemeCons', 'rest should return the rest of the list, i.e. a cons type.')
        self.assertEqual(str(obj), '(2 3)', 'the rest of (1 2 3) should be (2 3)')

    def test_eval_rest_toManyArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(rest (list 1 2 3) (list 2 3 4))')

    def test_eval_rest_tooFewArguments(self):
        self.assertRaises(schemeExceptions.ArgumentCountException, eval_string, '(rest)')

    def test_eval_rest_noListArgument(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(rest 1)')

    def test_eval_rest_emptyListArgument(self):
        self.assertRaises(schemeExceptions.ArgumentTypeException, eval_string, '(rest (list))')

    def test_eval_rest_listWithOneElement(self):
        obj = eval_string('(rest (list 1))')
        self.assertEqual(obj.type, 'schemeNil', 'rest should return the rest of the list (1), i.e. schemeNil.')
        self.assertEqual(str(obj), '()', 'the rest of (1) should be ()')








