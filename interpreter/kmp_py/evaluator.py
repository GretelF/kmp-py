from interpreter.kmp_py import schemeExceptions
from interpreter.kmp_py.scheme import *

class SchemeEvaluator(SchemeSingleton):

    syntaxEnv = SchemeEnvironment()
    #Bindings are added in schemeBuiltin.py

    # create global environment with builtin functions.
    globalEnv = SchemeEnvironment()
    globalEnv.parent = syntaxEnv
    #Bindings are added in schemeBuiltin.py


    def __init__(self):
        super().__init__()

    def evaluate(self, obj, env = None):
        if env is None:
            env = self.globalEnv

        if (obj.type == 'schemeSymbol'):
            retVal = env.getBinding(obj)
            if (retVal):
                return retVal
            else:
                if(env == self.globalEnv):
                    raise schemeExceptions.NoBindingException("No binding found for symbol {0} in the global environment.")
                raise schemeExceptions.NoBindingException("No binding found for symbol {0} in environment {1}".format(str(obj), str(env)))
        elif(obj.type == 'schemeCons'):
            if not obj.car.type == 'schemeSymbol':
                raise schemeExceptions.InvalidInputException("First element of list has to be a procedure.")                #TODO: not symbol but procedure

            proc = self.evaluate(obj.car, env)
            retVal = SchemeVoid()
            if proc.type == 'schemeBuiltinFunction':
                evaluatedArgsArray = []
                unevaluatedArgs = obj.cdr
                unevaluatedArgsArray = []
                if unevaluatedArgs.type == 'schemeCons':
                    unevaluatedArgsArray = unevaluatedArgs.toArray()
                for arg in unevaluatedArgsArray:
                    evaluatedArgsArray.append(self.evaluate(arg, env))
                retVal = proc.func(evaluatedArgsArray)
            elif (proc.type == 'schemeBuiltinSyntax'):
                unevaluatedArgs = obj.cdr
                unevaluatedArgsArray = []
                if unevaluatedArgs.type == 'schemeCons':
                    unevaluatedArgsArray = unevaluatedArgs.toArray()
                retVal = proc.func(unevaluatedArgsArray, env)
            else:                                                                   # UserDefinedFunction
                pass
            return retVal
        else:                                                                       #schemeTrue, schemeFalse, schemeNil, schemeNumber, schemeString,
            return obj

