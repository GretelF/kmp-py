from interpreter.kmp_py import schemeBuiltin, reader, scheme, schemeExceptions

class SchemeEvaluator():

    syntaxEnv = scheme.SchemeEnvironment()
    syntaxEnv.addBinding(scheme.SchemeSymbol('if'), scheme.SchemeBuiltinSyntax('if', schemeBuiltin.builtin_if))
    syntaxEnv.addBinding(scheme.SchemeSymbol('lambda'), scheme.SchemeBuiltinSyntax('lambda', schemeBuiltin.builtin_lambda))
    syntaxEnv.addBinding(scheme.SchemeSymbol('define'), scheme.SchemeBuiltinSyntax('define', schemeBuiltin.builtin_define))
    syntaxEnv.addBinding(scheme.SchemeSymbol('set'), scheme.SchemeBuiltinSyntax('set', schemeBuiltin.builtin_set))
    syntaxEnv.addBinding(scheme.SchemeSymbol('let'), scheme.SchemeBuiltinSyntax('let', schemeBuiltin.builtin_let))

    # create global environment with builtin functions.
    globalEnv = scheme.SchemeEnvironment()
    globalEnv.parent = syntaxEnv
    globalEnv.addBinding(scheme.SchemeSymbol('+'), scheme.SchemeBuiltinFunction('add', schemeBuiltin.builtin_add))
    globalEnv.addBinding(scheme.SchemeSymbol('-'), scheme.SchemeBuiltinFunction('sub', schemeBuiltin.builtin_sub))
    globalEnv.addBinding(scheme.SchemeSymbol('*'), scheme.SchemeBuiltinFunction('mul', schemeBuiltin.builtin_mul))
    globalEnv.addBinding(scheme.SchemeSymbol('/'), scheme.SchemeBuiltinFunction('div', schemeBuiltin.builtin_div))
    globalEnv.addBinding(scheme.SchemeSymbol('eq?'), scheme.SchemeBuiltinFunction('eq', schemeBuiltin.builtin_eq))
    globalEnv.addBinding(scheme.SchemeSymbol('='), scheme.SchemeBuiltinFunction('eq_arit', schemeBuiltin.builtin_eq_arit))
    globalEnv.addBinding(scheme.SchemeSymbol('print'), scheme.SchemeBuiltinFunction('print', schemeBuiltin.builtin_print))
    globalEnv.addBinding(scheme.SchemeSymbol('cons'), scheme.SchemeBuiltinFunction('cons', schemeBuiltin.builtin_cons))
    globalEnv.addBinding(scheme.SchemeSymbol('car'), scheme.SchemeBuiltinFunction('car', schemeBuiltin.builtin_car))
    globalEnv.addBinding(scheme.SchemeSymbol('cdr'), scheme.SchemeBuiltinFunction('cdr', schemeBuiltin.builtin_cdr))

    globalEnv.addBinding(scheme.SchemeSymbol('null'), scheme.SchemeNil())
    globalEnv.addBinding(scheme.SchemeSymbol('nil'), scheme.SchemeNil())
    globalEnv.addBinding(scheme.SchemeSymbol('empty'), scheme.SchemeNil())
    globalEnv.addBinding(scheme.SchemeSymbol('#f'), scheme.SchemeFalse())
    globalEnv.addBinding(scheme.SchemeSymbol('#t'), scheme.SchemeTrue())


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
                    proc = self.evaluate(obj.car, env)
                    retVal = scheme.SchemeVoid()
                    if (proc.type == 'schemeBuiltinFunction'):
                        evaluatedArgs = []
                        unevaluatedArgs = obj.cdr
                        while(unevaluatedArgs.type != 'schemeNil'):
                            latestArg = unevaluatedArgs.car
                            evaluatedArgs.append(self.evaluate(latestArg))
                            unevaluatedArgs = unevaluatedArgs.cdr

                        retVal = proc.func(evaluatedArgs)
                    elif (proc.type == 'schemeBuiltinSyntax'):
                        unevaluatedArgs = obj.cdr
                        retVal = proc.func(unevaluatedArgs)
                    else:                                                           # UserDefinedFunction
                        pass
                    return retVal
        else:                                               #schemeTrue, schemeFalse, schemeNil, schemeNumber, schemeString,
            return obj
