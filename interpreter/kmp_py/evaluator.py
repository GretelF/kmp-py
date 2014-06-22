from interpreter.kmp_py import schemeBuiltin, reader, scheme, schemeExceptions

class SchemeEvaluator():

    # create global environment with builtin functions.
    globalEnv = scheme.SchemeEnvironment()
    globalEnv.addBinding(scheme.SchemeSymbol('+'), schemeBuiltin.builtin_add)
    globalEnv.addBinding(scheme.SchemeSymbol('-'), schemeBuiltin.builtin_sub)
    globalEnv.addBinding(scheme.SchemeSymbol('*'), schemeBuiltin.builtin_mul)
    globalEnv.addBinding(scheme.SchemeSymbol('/'), schemeBuiltin.builtin_div)
    globalEnv.addBinding(scheme.SchemeSymbol('eq?'), schemeBuiltin.builtin_eq)


    def __init__(self):
        pass

    def eval_string(self, string, env = globalEnv):
        r = reader.SchemeReader()
        obj = r.read(scheme.SchemeStringStream(string))
        return self.evaluate(obj, env)

    def evaluate(self, obj, env = globalEnv):
        if (obj.type == 'schemeSymbol'):
            retVal = env.getBinding(obj)
            if (retVal):
                return retVal
            else:
                raise schemeExceptions.NoBindingException("No binding found for symbol {0} in environment {1}".format(str(obj), str(env)))
        elif(obj.type == 'schemeCons'):
            if(not obj.car.type == 'schemeSymbol'):
                raise schemeExceptions.InvalidInputException("First element of list has to be a procedure.")
            else:
                proc = self.evaluate(obj.car, env)
                evaluatedArgs = []
                unevaluatedArgs = obj.cdr
                while(unevaluatedArgs.type != 'schemeNil'):
                    latestArg = unevaluatedArgs.car
                    evaluatedArgs.append(self.evaluate(latestArg))
                    unevaluatedArgs = unevaluatedArgs.cdr

                retVal = proc(evaluatedArgs)
                return retVal
        else:                                               #schemeTrue, schemeFalse, schemeNil, schemeNumber, schemeString,
            return obj
