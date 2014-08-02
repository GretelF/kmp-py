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

class SchemePrimeTest(TestCase):
    def test_prime(self):
        eval_string('''
            (define (computePrimes num)
                (define (isPrime primes cur)
                    (if (eq? primes nil)
                        true
                        (if (= (% cur (first primes)) 0)
                            false
                            (isPrime (rest primes) cur)
                        )
                    )
                )
                (define (helper primes cur i)
                    (if (= num i)
                        primes
                        (if (isPrime primes cur)
                            (helper
                                (cons cur primes)
                                (+ cur 1)
                                (+ i 1))
                            (helper primes (+ cur 1) i)
                        )
                    )
                )
                (helper (cons 2 nil) 3 1)
            )''')
        obj = eval_string('computePrimes')
        self.assertEqual(obj.type, 'schemeUserDefinedFunction', 'computePrimes should be a user defined function.')

        primes = eval_string('(computePrimes 5)')
        self.assertEqual(str(primes), '(11 7 5 3 2)', 'computePrimes does not compute the first 5 primes correctly.')

        eval_string('(recursion-limit 10000)')
        time = eval_string('(time computePrimes 50)')
        print(time)

