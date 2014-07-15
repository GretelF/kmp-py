from interpreter.kmp_py import scheme,schemeExceptions,evaluator

def builtin_add(evaluatedArgs):
    retVal = 0
    for operand in evaluatedArgs:
        if(operand.type != 'schemeNumber'):
            raise schemeExceptions.ArgumentTypeException('{0} is no valid operand for procedure +'. format(str(operand)))
        retVal += operand.value
    return scheme.SchemeNumber(retVal)

def builtin_sub(evaluatedArgs):
    retVal = evaluatedArgs[0].value
    for operand in evaluatedArgs[1:]:
        if(operand.type != 'schemeNumber'):
            raise schemeExceptions.ArgumentTypeException('{0} is no valid operand for procedure +'. format(str(operand)))
        retVal -= operand.value
    return scheme.SchemeNumber(retVal)

def builtin_mul(evaluatedArgs):
    retVal = 1
    for operand in evaluatedArgs:
        if(operand.type != 'schemeNumber'):
            raise schemeExceptions.ArgumentTypeException('{0} is no valid operand for procedure +'. format(str(operand)))
        retVal *= operand.value
    return scheme.SchemeNumber(retVal)

def builtin_div(evaluatedArgs):
    retVal = evaluatedArgs[0].value
    for operand in evaluatedArgs[1:]:
        if(operand.type != 'schemeNumber'):
            raise schemeExceptions.ArgumentTypeException('{0} is no valid operand for procedure +'. format(str(operand)))
        retVal /= operand.value
    return scheme.SchemeNumber(retVal)

def builtin_eq(evaluatedArgs):
    if(len(evaluatedArgs)>2):
        raise schemeExceptions.ArgumentCountException('eq? expects exactly 2 arguments.')
    return scheme.SchemeTrue() if (evaluatedArgs[0]==evaluatedArgs[1]) else scheme.SchemeFalse()

def builtin_eq_arit(evaluatedArgs):
    if(len(evaluatedArgs)>2):
        raise schemeExceptions.ArgumentCountException('= expects exactly 2 arguments.')
    if(evaluatedArgs[0].type != 'schemeNumber' or evaluatedArgs[1].type != 'schemeNumber'):
        raise schemeExceptions.ArgumentTypeException('= expects two numbers')
    else:
        return scheme.SchemeTrue() if (evaluatedArgs[0].value == evaluatedArgs[1].value) else scheme.SchemeFalse()

def builtin_cons(evaluatedArgs):
    if(len(evaluatedArgs)>2):
        raise schemeExceptions.ArgumentCountException('cons expects exactly 2 arguments.')
    return scheme.SchemeCons(evaluatedArgs[0], evaluatedArgs[1])

def builtin_car(evaluatedArgs):
    if(len(evaluatedArgs)>1):
        raise schemeExceptions.ArgumentCountException('car expects exactly 1 argument.')
    if(evaluatedArgs[0].type != 'schemeCons'):
        raise schemeExceptions.InvalidInputException('car expects cons as argument')
    return evaluatedArgs[0].car

def builtin_cdr(evaluatedArgs):
    if(len(evaluatedArgs)>1):
        raise schemeExceptions.ArgumentCountException('cdr expects exactly 1 argument.')
    if(evaluatedArgs[0].type != 'schemeCons'):
        raise schemeExceptions.ArgumentTypeException('cdr expects cons as argument')
    return evaluatedArgs[0].cdr

def builtin_print(evaluatedArgs):
    if(len(evaluatedArgs)>1):
        raise schemeExceptions.ArgumentCountException('print expects exactly 1 argument.')
    print(str(evaluatedArgs[0]))                                                #TODO print in REPL
    return scheme.SchemeVoid()

def builtin_write():
    pass

def builtin_display():
    pass

def builtin_quote():
    pass



# Syntax

def evaluate(arg, env):
    return evaluator.SchemeEvaluator().evaluate(arg, env)           # SchemeEvaluator is singleton


def builtin_begin(unevaluatedArgs, env):
    pass

def builtin_define(unevaluatedArgs, env):
    if len(unevaluatedArgs) != 2:
        raise schemeExceptions.ArgumentCountException('define expects exactly 2 arguments.')
    if unevaluatedArgs[0].type != 'schemeSymbol':
        raise schemeExceptions.ArgumentTypeException('define expects schemeSymbol as first argument.')
    env.addBinding(unevaluatedArgs[0], unevaluatedArgs[1])
    return scheme.SchemeVoid()

def builtin_lambda(unevaluatedArgs, env):
    pass

def builtin_if(unevaluatedArgs, env):
    if len(unevaluatedArgs) != 3:
        raise schemeExceptions.ArgumentCountException('if expects exactly 3 arguments.')
    condition = evaluate(unevaluatedArgs[0], env)
    if condition.isTrue():
        return evaluate(unevaluatedArgs[1], env)
    return evaluate(unevaluatedArgs[2], env)


def builtin_set(unevaluatedArgs, env):
    if len(unevaluatedArgs) != 2:
        raise schemeExceptions.ArgumentCountException('set! expects exactly 2 arguments.')
    symbol = unevaluatedArgs[0]
    if symbol.type != 'schemeSymbol':
        raise schemeExceptions.ArgumentTypeException('set! expects schemeSymbol as first argument.')
    success = env.setBinding(symbol, unevaluatedArgs[1])
    if not success:
        raise schemeExceptions.NoBindingException('No Binding found for symbol {0} in environment {1}'.format(symbol, env))
    return scheme.SchemeVoid()

def builtin_let(unevaluatedArgs, env):
    pass





def initializeBindings():
    # add builtins to environments
    syntaxEnv = evaluator.SchemeEvaluator.syntaxEnv
    syntaxEnv.addBinding(scheme.SchemeSymbol('if'), scheme.SchemeBuiltinSyntax('if', builtin_if))
    syntaxEnv.addBinding(scheme.SchemeSymbol('lambda'), scheme.SchemeBuiltinSyntax('lambda', builtin_lambda))
    syntaxEnv.addBinding(scheme.SchemeSymbol('define'), scheme.SchemeBuiltinSyntax('define', builtin_define))
    syntaxEnv.addBinding(scheme.SchemeSymbol('set!'), scheme.SchemeBuiltinSyntax('set', builtin_set))
    syntaxEnv.addBinding(scheme.SchemeSymbol('let'), scheme.SchemeBuiltinSyntax('let', builtin_let))

    globalEnv = evaluator.SchemeEvaluator.globalEnv
    globalEnv.addBinding(scheme.SchemeSymbol('+'), scheme.SchemeBuiltinFunction('add', builtin_add))
    globalEnv.addBinding(scheme.SchemeSymbol('-'), scheme.SchemeBuiltinFunction('sub', builtin_sub))
    globalEnv.addBinding(scheme.SchemeSymbol('*'), scheme.SchemeBuiltinFunction('mul', builtin_mul))
    globalEnv.addBinding(scheme.SchemeSymbol('/'), scheme.SchemeBuiltinFunction('div', builtin_div))
    globalEnv.addBinding(scheme.SchemeSymbol('eq?'), scheme.SchemeBuiltinFunction('eq', builtin_eq))
    globalEnv.addBinding(scheme.SchemeSymbol('='), scheme.SchemeBuiltinFunction('eq_arit', builtin_eq_arit))
    globalEnv.addBinding(scheme.SchemeSymbol('print'), scheme.SchemeBuiltinFunction('print', builtin_print))
    globalEnv.addBinding(scheme.SchemeSymbol('cons'), scheme.SchemeBuiltinFunction('cons', builtin_cons))
    globalEnv.addBinding(scheme.SchemeSymbol('car'), scheme.SchemeBuiltinFunction('car', builtin_car))
    globalEnv.addBinding(scheme.SchemeSymbol('cdr'), scheme.SchemeBuiltinFunction('cdr', builtin_cdr))

    globalEnv.addBinding(scheme.SchemeSymbol('null'), scheme.SchemeNil())
    globalEnv.addBinding(scheme.SchemeSymbol('nil'), scheme.SchemeNil())
    globalEnv.addBinding(scheme.SchemeSymbol('empty'), scheme.SchemeNil())
    globalEnv.addBinding(scheme.SchemeSymbol('#f'), scheme.SchemeFalse())
    globalEnv.addBinding(scheme.SchemeSymbol('#t'), scheme.SchemeTrue())