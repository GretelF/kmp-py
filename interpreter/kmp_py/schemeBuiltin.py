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

def builtin_cons():
    pass

def builtin_car():
    pass

def builtin_cdr():
    pass

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

def builtin_begin():
    pass