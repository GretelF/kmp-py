from interpreter.kmp_py import schemeExceptions
from interpreter.kmp_py.scheme import SchemeVoid, SchemeSingleton, SchemeEnvironment

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
                raise schemeExceptions.NoBindingException("No binding found for symbol {0}".format(str(obj)))
        elif(obj.type == 'schemeCons'):
            proc = self.evaluate(obj.car, env)
            retVal = SchemeVoid()
            if proc.type in ('schemeBuiltinFunction', 'schemeUserDefinedFunction'):
                evaluatedArgsArray = []
                unevaluatedArgs = obj.cdr
                unevaluatedArgsArray = []
                if unevaluatedArgs.type == 'schemeCons':
                    unevaluatedArgsArray = unevaluatedArgs.toArray()
                for arg in unevaluatedArgsArray:
                    evaluatedArgsArray.append(self.evaluate(arg, env))
                retVal = proc.call(evaluatedArgsArray)
            elif (proc.type == 'schemeBuiltinSyntax'):
                unevaluatedArgs = obj.cdr
                unevaluatedArgsArray = []
                if unevaluatedArgs.type == 'schemeCons':
                    unevaluatedArgsArray = unevaluatedArgs.toArray()
                retVal = proc.func(unevaluatedArgsArray, env)
            else:
                raise schemeExceptions.ArgumentTypeException('First argument has to be syntax or procedure')
            return retVal
        else:                                                                       #schemeTrue, schemeFalse, schemeNil, schemeNumber, schemeString,
            return obj

