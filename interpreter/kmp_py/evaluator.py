from interpreter.kmp_py import schemeBuiltin, reader, scheme, schemeExceptions

class SchemeEvaluator():

    syntaxEnv = scheme.SchemeEnvironment()
    syntaxEnv.addBinding(scheme.SchemeSymbol('if'), schemeBuiltin.builtin_if)
    syntaxEnv.addBinding(scheme.SchemeSymbol('lambda'), schemeBuiltin.builtin_lambda)
    syntaxEnv.addBinding(scheme.SchemeSymbol('define'), schemeBuiltin.builtin_define)
    syntaxEnv.addBinding(scheme.SchemeSymbol('set'), schemeBuiltin.builtin_set)
    syntaxEnv.addBinding(scheme.SchemeSymbol('let'), schemeBuiltin.builtin_let)

    # create global environment with builtin functions.
    globalEnv = scheme.SchemeEnvironment()
    globalEnv.addBinding(scheme.SchemeSymbol('+'), schemeBuiltin.builtin_add)
    globalEnv.addBinding(scheme.SchemeSymbol('-'), schemeBuiltin.builtin_sub)
    globalEnv.addBinding(scheme.SchemeSymbol('*'), schemeBuiltin.builtin_mul)
    globalEnv.addBinding(scheme.SchemeSymbol('/'), schemeBuiltin.builtin_div)
    globalEnv.addBinding(scheme.SchemeSymbol('eq?'), schemeBuiltin.builtin_eq)
    globalEnv.addBinding(scheme.SchemeSymbol('print'), schemeBuiltin.builtin_print)
    globalEnv.addBinding(scheme.SchemeSymbol('cons'), schemeBuiltin.builtin_cons)
    globalEnv.addBinding(scheme.SchemeSymbol('car'), schemeBuiltin.builtin_car)
    globalEnv.addBinding(scheme.SchemeSymbol('cdr'), schemeBuiltin.builtin_cdr)


    globalEnv.addBinding(scheme.SchemeSymbol('null'), scheme.SchemeNil())
    globalEnv.addBinding(scheme.SchemeSymbol('nil'), scheme.SchemeNil())


    def __init__(self):
        pass

    def evaluate(self, obj, env = globalEnv):
        if (obj.type == 'schemeSymbol'):
            retVal = env.getBinding(obj)
            if (retVal):
                return retVal
            else:
                if(env == self.globalEnv):
                    raise schemeExceptions.NoBindingException("No binding found for symbol {0} in the global environment.")
                raise schemeExceptions.NoBindingException("No binding found for symbol {0} in environment {1}".format(str(obj), str(env)))
        elif(obj.type == 'schemeCons'):
            if(not obj.car.type == 'schemeSymbol'):
                raise schemeExceptions.InvalidInputException("First element of list has to be a procedure.")                #TODO: not symbol but procedure
            else:
                try:
                    syntax = self.evaluate(obj.car, self.syntaxEnv)
                    return syntax
                except:
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
