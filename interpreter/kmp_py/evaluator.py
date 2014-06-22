from interpreter.kmp_py import reader, scheme, schemeExceptions

class SchemeEvaluator():
    def __init__(self):
        pass

    def eval(self, string, env = None):
        r = reader.SchemeReader()
        obj = r.read(scheme.SchemeStringStream(string))

        if (obj.type == 'schemeNumber' or obj.type == 'schemeString'):
            return obj
        elif (obj.type == 'schemeSymbol'):
            retVal = env.getBinding(obj)
            if (retVal):
                return retVal
            else:
                raise schemeExceptions.NoBindingException("No binding found for symbol {0} in environment {1}".format(str(obj), str(env)))
