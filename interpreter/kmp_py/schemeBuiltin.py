from interpreter.kmp_py import schemeExceptions,evaluator
from interpreter.kmp_py.scheme import *

def builtin_add(evaluatedArgs):
    retVal = 0
    for operand in evaluatedArgs:
        if(operand.type != 'schemeNumber'):
            raise schemeExceptions.ArgumentTypeException('{0} is no valid operand for procedure +'. format(str(operand)))
        retVal += operand.value
    return SchemeNumber(retVal)

def builtin_sub(evaluatedArgs):
    retVal = evaluatedArgs[0].value
    for operand in evaluatedArgs[1:]:
        if(operand.type != 'schemeNumber'):
            raise schemeExceptions.ArgumentTypeException('{0} is no valid operand for procedure -'. format(str(operand)))
        retVal -= operand.value
    return SchemeNumber(retVal)

def builtin_mul(evaluatedArgs):
    retVal = 1
    for operand in evaluatedArgs:
        if(operand.type != 'schemeNumber'):
            raise schemeExceptions.ArgumentTypeException('{0} is no valid operand for procedure *'. format(str(operand)))
        retVal *= operand.value
    return SchemeNumber(retVal)

def builtin_div(evaluatedArgs):
    retVal = evaluatedArgs[0].value
    for operand in evaluatedArgs[1:]:
        if(operand.type != 'schemeNumber'):
            raise schemeExceptions.ArgumentTypeException('{0} is no valid operand for procedure /'. format(str(operand)))
        retVal /= operand.value
    return SchemeNumber(retVal)

def builtin_eq(evaluatedArgs):
    if(len(evaluatedArgs)>2):
        raise schemeExceptions.ArgumentCountException('eq? expects exactly 2 arguments.')
    return SchemeTrue() if (evaluatedArgs[0]==evaluatedArgs[1]) else SchemeFalse()

def builtin_eq_arit(evaluatedArgs):
    if(len(evaluatedArgs)>2):
        raise schemeExceptions.ArgumentCountException('= expects exactly 2 arguments.')
    if(evaluatedArgs[0].type != 'schemeNumber' or evaluatedArgs[1].type != 'schemeNumber'):
        raise schemeExceptions.ArgumentTypeException('= expects two numbers')
    else:
        return SchemeTrue() if (evaluatedArgs[0].value == evaluatedArgs[1].value) else SchemeFalse()

def builtin_cons(evaluatedArgs):
    if(len(evaluatedArgs)>2):
        raise schemeExceptions.ArgumentCountException('cons expects exactly 2 arguments.')
    return SchemeCons(evaluatedArgs[0], evaluatedArgs[1])

def builtin_car(evaluatedArgs):
    if(len(evaluatedArgs)>1):
        raise schemeExceptions.ArgumentCountException('car expects exactly 1 argument.')
    if(evaluatedArgs[0].type != 'schemeCons'):
        raise schemeExceptions.ArgumentTypeException('car expects cons as argument')
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
    return SchemeVoid()

def builtin_write():
    pass

def builtin_display():
    pass



# Syntax

def evaluate(arg, env):
    return evaluator.SchemeEvaluator().evaluate(arg, env)           # SchemeEvaluator is singleton


def builtin_begin(unevaluatedArgs, env):
    pass

def builtin_define(unevaluatedArgs, env):
    if len(unevaluatedArgs) != 2:
        raise schemeExceptions.ArgumentCountException('define expects exactly 2 arguments.')

    symbol = unevaluatedArgs[0]
    unevaluatedValue = unevaluatedArgs[1]

    if symbol.type != 'schemeSymbol':
        raise schemeExceptions.ArgumentTypeException('define expects schemeSymbol as first argument.')

    evaluatedValue = evaluate(unevaluatedValue, env)
    if evaluatedValue.type == 'schemeUserDefinedFunction' and evaluatedValue.name is None:
        evaluatedValue.name = symbol.value

    env.addBinding(symbol, evaluatedValue)
    return SchemeVoid()

def builtin_lambda(unevaluatedArgs, env):
    if len(unevaluatedArgs) < 2:
        raise schemeExceptions.ArgumentCountException('lambda expects at least 2 arguments.')
    lambdaArguments = unevaluatedArgs[0]
    lambdaBody = unevaluatedArgs[1:]
    if lambdaArguments.type not in ('schemeCons', 'schemeNil'):                 # TODO: Maybe too strict. What about Symbols?
        raise schemeExceptions.ArgumentTypeException('lambda expects a list (cons) or nil as first argument.')
    return SchemeUserDefinedFunction(lambdaArguments.toArray(),lambdaBody, env)

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
    return SchemeVoid()

def builtin_let(unevaluatedArgs, env):
    pass

def builtin_quote(unevaluatedArgs, env):
    if len(unevaluatedArgs)>1:
        raise schemeExceptions.ArgumentCountException('quote expects exactly 1 argument.')
    return unevaluatedArgs[0]





def initializeBindings():
    # add builtins to environments
    syntaxEnv = evaluator.SchemeEvaluator.syntaxEnv
    syntaxEnv.addBinding(SchemeSymbol('if'), SchemeBuiltinSyntax('if', builtin_if))
    syntaxEnv.addBinding(SchemeSymbol('lambda'), SchemeBuiltinSyntax('lambda', builtin_lambda))
    syntaxEnv.addBinding(SchemeSymbol('define'), SchemeBuiltinSyntax('define', builtin_define))
    syntaxEnv.addBinding(SchemeSymbol('set!'), SchemeBuiltinSyntax('set', builtin_set))
    syntaxEnv.addBinding(SchemeSymbol('let'), SchemeBuiltinSyntax('let', builtin_let))
    syntaxEnv.addBinding(SchemeSymbol('quote'), SchemeBuiltinSyntax('quote', builtin_quote))

    globalEnv = evaluator.SchemeEvaluator.globalEnv
    globalEnv.addBinding(SchemeSymbol('+'), SchemeBuiltinFunction('add', builtin_add))
    globalEnv.addBinding(SchemeSymbol('-'), SchemeBuiltinFunction('sub', builtin_sub))
    globalEnv.addBinding(SchemeSymbol('*'), SchemeBuiltinFunction('mul', builtin_mul))
    globalEnv.addBinding(SchemeSymbol('/'), SchemeBuiltinFunction('div', builtin_div))
    globalEnv.addBinding(SchemeSymbol('eq?'), SchemeBuiltinFunction('eq', builtin_eq))
    globalEnv.addBinding(SchemeSymbol('='), SchemeBuiltinFunction('eq_arit', builtin_eq_arit))
    globalEnv.addBinding(SchemeSymbol('print'), SchemeBuiltinFunction('print', builtin_print))
    globalEnv.addBinding(SchemeSymbol('cons'), SchemeBuiltinFunction('cons', builtin_cons))
    globalEnv.addBinding(SchemeSymbol('car'), SchemeBuiltinFunction('car', builtin_car))
    globalEnv.addBinding(SchemeSymbol('cdr'), SchemeBuiltinFunction('cdr', builtin_cdr))

    globalEnv.addBinding(SchemeSymbol('null'), SchemeNil())
    globalEnv.addBinding(SchemeSymbol('nil'), SchemeNil())
    globalEnv.addBinding(SchemeSymbol('empty'), SchemeNil())
    globalEnv.addBinding(SchemeSymbol('#f'), SchemeFalse())
    globalEnv.addBinding(SchemeSymbol('#t'), SchemeTrue())