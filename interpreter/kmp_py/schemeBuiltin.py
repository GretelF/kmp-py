from interpreter.kmp_py import scheme,schemeExceptions

def builtin_add(evaluatedArgs):
    retVal = 0
    for operand in evaluatedArgs:
        if(operand.type != 'schemeNumber'):
            raise schemeExceptions.InvalidInputException('{0} is no valid operand for procedure +'. format(str(operand)))
        retVal += operand.value
    return scheme.SchemeNumber(retVal)

def builtin_sub(evaluatedArgs):
    retVal = evaluatedArgs[0].value
    for operand in evaluatedArgs[1:]:
        if(operand.type != 'schemeNumber'):
            raise schemeExceptions.InvalidInputException('{0} is no valid operand for procedure +'. format(str(operand)))
        retVal -= operand.value
    return scheme.SchemeNumber(retVal)

def builtin_mul(evaluatedArgs):
    retVal = 1
    for operand in evaluatedArgs:
        if(operand.type != 'schemeNumber'):
            raise schemeExceptions.InvalidInputException('{0} is no valid operand for procedure +'. format(str(operand)))
        retVal *= operand.value
    return scheme.SchemeNumber(retVal)

def builtin_div(evaluatedArgs):
    retVal = evaluatedArgs[0].value
    for operand in evaluatedArgs[1:]:
        if(operand.type != 'schemeNumber'):
            raise schemeExceptions.InvalidInputException('{0} is no valid operand for procedure +'. format(str(operand)))
        retVal /= operand.value
    return scheme.SchemeNumber(retVal)

def builtin_eq(evaluatedArgs):
    if(len(evaluatedArgs)>2):
        raise schemeExceptions.InvalidInputException('eq? expects exactly 2 arguments.')
    if(evaluatedArgs[0]==evaluatedArgs[1]):
        return scheme.SchemeTrue()
    else:
        return scheme.SchemeFalse()

def builtin_cons(evaluatedArgs):
    if(len(evaluatedArgs)>2):
        raise schemeExceptions.InvalidInputException('cons expects exactly 2 arguments.')
    return scheme.SchemeCons(evaluatedArgs[0], evaluatedArgs[1])

def builtin_car(evaluatedArgs):
    if(len(evaluatedArgs)>1):
        raise schemeExceptions.InvalidInputException('car expects exactly 1 arguments.')
    if(evaluatedArgs[0].type != 'schemeCons'):
        raise schemeExceptions.InvalidInputException('car expects cons as argument')
    return evaluatedArgs[0].car

def builtin_cdr(evaluatedArgs):
    if(len(evaluatedArgs)>1):
        raise schemeExceptions.InvalidInputException('cdr expects exactly 1 arguments.')
    if(evaluatedArgs[0].type != 'schemeCons'):
        raise schemeExceptions.InvalidInputException('cdr expects cons as argument')
    return evaluatedArgs[0].cdr

def builtin_print(evaluatedArgs):
    if(len(evaluatedArgs)>1):
        raise schemeExceptions.InvalidInputException('print expects exactly 1 arguments.')
    print(str(evaluatedArgs[0]))                                                #TODO print in REPL
    return scheme.SchemeVoid()

def builtin_write():
    pass

def builtin_display():
    pass

def builtin_quote():
    pass



# Syntax

def builtin_begin():
    pass

def builtin_define():
    pass

def builtin_lambda():
    pass

def builtin_if():
    pass

def builtin_set():
    pass

def builtin_let():
    pass
