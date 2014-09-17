import sys, time, os
from interpreter.kmp_py import schemeExceptions,evaluator, reader
from interpreter.kmp_py.scheme import *

def builtin_exit(evaluatedArgs):
    exitcode = 0
    if len(evaluatedArgs)>0 and evaluatedArgs[0].type == 'schemeNumber':
        exitcode = int(evaluatedArgs[0].value)
    sys.exit(exitcode)

# arithmetic builtin functions:

def builtin_add(evaluatedArgs):
    retVal = 0
    for operand in evaluatedArgs:
        if(operand.type != 'schemeNumber'):
            raise schemeExceptions.ArgumentTypeException('{0} is no valid operand for function +.'. format(str(operand)))
        retVal += operand.value
    return SchemeNumber(retVal)

def builtin_sub(evaluatedArgs):
    if len(evaluatedArgs) < 1:
        raise schemeExceptions.ArgumentCountException('function - expects at least 1 argument.')
    for operand in evaluatedArgs:
        if(operand.type != 'schemeNumber'):
            raise schemeExceptions.ArgumentTypeException('{0} is no valid operand for function -.'. format(str(operand)))
    retVal = evaluatedArgs[0].value
    if len(evaluatedArgs) == 1:
        return SchemeNumber(-retVal)
    for operand in evaluatedArgs[1:]:
        retVal -= operand.value
    return SchemeNumber(retVal)

def builtin_mul(evaluatedArgs):
    retVal = 1
    for operand in evaluatedArgs:
        if(operand.type != 'schemeNumber'):
            raise schemeExceptions.ArgumentTypeException('{0} is no valid operand for function *.'. format(str(operand)))
        retVal *= operand.value
    return SchemeNumber(retVal)

def builtin_div(evaluatedArgs):
    if len(evaluatedArgs) < 1:
        raise schemeExceptions.ArgumentCountException('function / expects at least 1 argument.')
    for operand in evaluatedArgs:
        if(operand.type != 'schemeNumber'):
            raise schemeExceptions.ArgumentTypeException('{0} is no valid operand for procedure /.'.format(str(operand)))
        if(operand.value == 0):
            raise schemeExceptions.DivisionByZero('Invalid input! Cannot divide by zero.')
    retVal = evaluatedArgs[0].value
    if len(evaluatedArgs) == 1:
        return SchemeNumber(1/retVal)
    for operand in evaluatedArgs[1:]:
        retVal /= operand.value
    return SchemeNumber(retVal)

def builtin_modulo(evaluatedArgs):
    if len(evaluatedArgs) != 2:
        raise schemeExceptions.ArgumentCountException('function % expects exactly 2 arguments.')
    for operand in evaluatedArgs:
        if(operand.type != 'schemeNumber'):
            raise schemeExceptions.ArgumentTypeException('{0} is no valid operand for procedure %. Expects SchemeNumber.'.format(str(operand)))
    for operand in evaluatedArgs:
        if (not isinstance(operand.value, int)):
            raise schemeExceptions.ArgumentTypeException('{0} is no valid operand for procedure %. Expects integer.'.format(str(operand)))
    if evaluatedArgs[1].value == 0:
        raise schemeExceptions.DivisionByZero('Second argument should not be 0.')
    return SchemeNumber(evaluatedArgs[0].value % evaluatedArgs[1].value)

def builtin_gt(evaluatedArgs):
    if(len(evaluatedArgs)!=2):
        raise schemeExceptions.ArgumentCountException('> expects exactly 2 arguments.')
    return SchemeTrue() if (evaluatedArgs[0].value > evaluatedArgs[1].value) else SchemeFalse()

def builtin_geqt(evaluatedArgs):
    if(len(evaluatedArgs)!=2):
        raise schemeExceptions.ArgumentCountException('>= expects exactly 2 arguments.')
    return SchemeTrue() if (evaluatedArgs[0].value >= evaluatedArgs[1].value) else SchemeFalse()

def builtin_lt(evaluatedArgs):
    if(len(evaluatedArgs)!=2):
        raise schemeExceptions.ArgumentCountException('< expects exactly 2 arguments.')
    return SchemeTrue() if (evaluatedArgs[0].value < evaluatedArgs[1].value) else SchemeFalse()

def builtin_leqt(evaluatedArgs):
    if(len(evaluatedArgs)!=2):
        raise schemeExceptions.ArgumentCountException('<= expects exactly 2 arguments.')
    return SchemeTrue() if (evaluatedArgs[0].value <= evaluatedArgs[1].value) else SchemeFalse()

def builtin_eq_arit(evaluatedArgs):
    if(len(evaluatedArgs)!=2):
        raise schemeExceptions.ArgumentCountException('= expects exactly 2 arguments.')
    if(evaluatedArgs[0].type != 'schemeNumber' or evaluatedArgs[1].type != 'schemeNumber'):
        raise schemeExceptions.ArgumentTypeException('= expects two numbers')
    else:
        return SchemeTrue() if (evaluatedArgs[0].value == evaluatedArgs[1].value) else SchemeFalse()

def builtin_abs(evaluatedArgs):
    if(len(evaluatedArgs)!=1):
        raise schemeExceptions.ArgumentCountException('abs expects exactly 1 arguments.')
    if evaluatedArgs[0].type != 'schemeNumber':
        raise schemeExceptions.ArgumentTypeException('{0} is no valid input for function abs. SchemeNumber expected.'.format(evaluatedArgs[0].type))
    retVal = evaluatedArgs[0].value
    if(retVal < 0):
        return SchemeNumber(-retVal)
    return SchemeNumber(retVal)


#builtin functions

def builtin_eq(evaluatedArgs):
    if(len(evaluatedArgs)!=2):
        raise schemeExceptions.ArgumentCountException('eq? expects exactly 2 arguments.')
    return SchemeTrue() if (evaluatedArgs[0] == evaluatedArgs[1]) else SchemeFalse()

def builtin_cons(evaluatedArgs):
    if(len(evaluatedArgs)!=2):
        raise schemeExceptions.ArgumentCountException('cons expects exactly 2 arguments.')
    return SchemeCons(evaluatedArgs[0], evaluatedArgs[1])

def builtin_car(evaluatedArgs):
    if(len(evaluatedArgs)!=1):
        raise schemeExceptions.ArgumentCountException('car expects exactly 1 argument.')
    if(evaluatedArgs[0].type != 'schemeCons'):
        raise schemeExceptions.ArgumentTypeException('car expects cons as argument')
    return evaluatedArgs[0].car

def builtin_cdr(evaluatedArgs):
    if(len(evaluatedArgs)!=1):
        raise schemeExceptions.ArgumentCountException('cdr expects exactly 1 argument.')
    if(evaluatedArgs[0].type != 'schemeCons'):
        raise schemeExceptions.ArgumentTypeException('cdr expects cons as argument')
    return evaluatedArgs[0].cdr

def builtin_list(evaluatedArgs):
    list = SchemeNil()
    for arg in evaluatedArgs[-1::-1]:
        list = SchemeCons(arg, list)
    return list

def builtin_first(evaluatedArgs):
    if len(evaluatedArgs) != 1:
        raise schemeExceptions.ArgumentCountException('first expects exactly 1 argument')
    arg = evaluatedArgs[0]
    if arg.type != 'schemeCons' or not arg.isRegular:
        raise schemeExceptions.ArgumentTypeException('first expects a not empty regular list as argument.')
    return evaluatedArgs[0].car

def builtin_rest(evaluatedArgs):
    if len(evaluatedArgs) != 1:
        raise schemeExceptions.ArgumentCountException('rest expects exactly 1 argument')
    arg = evaluatedArgs[0]
    if arg.type != 'schemeCons' or not arg.isRegular:
        raise schemeExceptions.ArgumentTypeException('rest expects a not empty regular list as argument.')
    return evaluatedArgs[0].cdr

def builtin_time(evaluatedArgs):
    if len(evaluatedArgs) < 1:
        raise schemeExceptions.ArgumentCountException('time expects at least 1 argument.')
    lambdaObject = evaluatedArgs[0]
    if lambdaObject.type not in ('schemeUserDefinedFunction','schemeBuiltinFunction'):
        raise schemeExceptions.ArgumentTypeException('first argument has to be callable.')
    args = evaluatedArgs[1:]
    toCall = lambdaObject.call
    before = now()
    toCall(args)
    after = now()
    elapsedTime = after - before
    return SchemeNumber(elapsedTime)

def now():
    return time.clock()

def builtin_recursionlimit(evaluatedArgs):
    if len(evaluatedArgs) == 0:
        return SchemeNumber(sys.getrecursionlimit())
    if len(evaluatedArgs) > 1:
        raise schemeExceptions.ArgumentCountException('recursion-limit expects at most 1 argument.')
    if evaluatedArgs[0].type != 'schemeNumber':
        raise schemeExceptions.ArgumentTypeException('recursion-limit expects schemeNumber as argument.')
    sys.setrecursionlimit(evaluatedArgs[0].value)
    return SchemeVoid()

def builtin_print(evaluatedArgs):
    if(len(evaluatedArgs)!=1):
        raise schemeExceptions.ArgumentCountException('print expects exactly 1 argument.')
    print(str(evaluatedArgs[0]))
    return SchemeVoid()

def builtin_display(evaluatedArgs):
    if(len(evaluatedArgs)!=1):
        raise schemeExceptions.ArgumentCountException('display expects exactly 1 argument.')
    print(evaluatedArgs[0].value)
    return SchemeVoid()

def builtin_type(evaluatedArgs):
    if (len(evaluatedArgs)!=1):
        raise schemeExceptions.ArgumentCountException('type? expects exactly 1 argument.')
    return SchemeString(evaluatedArgs[0].type)

def builtin_isList(evaluatedArgs):
    if (len(evaluatedArgs)!=1):
        raise schemeExceptions.ArgumentCountException('list? expects exactly 1 argument.')
    arg = evaluatedArgs[0]
    if arg.type not in ('schemeCons', 'schemeNil'):
        return SchemeFalse()
    if arg.type == 'schemeNil' or arg.isRegular():
        return SchemeTrue()
    return SchemeFalse()

def builtin_not(evaluatedArgs):
    if (len(evaluatedArgs) != 1):
        raise schemeExceptions.ArgumentCountException('not expects exactly 1 argument.')
    return SchemeTrue() if evaluatedArgs[0].isFalse() else SchemeFalse()

def builtin_map(evaluatedArgs):
    if len(evaluatedArgs) < 2:
        raise schemeExceptions.ArgumentCountException('map expects at least 2 arguments.')
    function = evaluatedArgs[0]
    lists = evaluatedArgs[1:]
    listArray = []
    if (function.type not in ('schemeUserDefinedFunction', 'schemeBuiltinFunction')):
        raise schemeExceptions.ArgumentTypeException('map expects callable object as first argument')
    for lst in lists:
        if lst.type not in ('schemeCons', 'schemeNil'):
            raise schemeExceptions.ArgumentTypeException('map expects schemeCons as second and further arguments.')
        array = lst.toArray()
        array.reverse()
        listArray.append(array)
    listLen = len(listArray[0])
    for lst in listArray:
        if len(lst) != listLen:
            raise schemeExceptions.InvalidInputException('all lists must have same size.')
    retVal = SchemeNil()
    for index in range(listLen):
        car = function.call(list(x[index] for x in listArray))
        cdr = retVal
        retVal = SchemeCons(car, cdr)
    return retVal

def builtin_getfunctioninfo(evaluatedArgs):
    if len(evaluatedArgs) != 1:
        raise schemeExceptions.ArgumentCountException('get-function-body expects exactly one argument')
    lambdaObject = evaluatedArgs[0]
    if lambdaObject.type != 'schemeUserDefinedFunction':
        raise schemeExceptions.ArgumentTypeException('get-function-body expects user defined function as argument.')
    arglist = lambdaObject.arglist
    bodylist = lambdaObject.bodylist
    if lambdaObject.name:
        builtin_display([SchemeString("name: {0}".format(lambdaObject.name))])
    builtin_display([SchemeString("arglist:")])
    for arg in arglist:
        builtin_display([SchemeString("    {0}".format(str(arg)))])
    builtin_display([SchemeString("bodylist:")])
    for part in bodylist:
        builtin_display([SchemeString("    {0}".format(str(part)))])
    return SchemeVoid()

def builtin_evalfile(evaluatedArgs):
    if len(evaluatedArgs) != 1:
        raise schemeExceptions.ArgumentCountException('eval-file expects exactly one argument')
    filepath = evaluatedArgs[0]
    if filepath.type != 'schemeString':
        raise schemeExceptions.ArgumentTypeException('eval-file expects SchemeString as argument')
    code = ''
    try:
        with open(filepath.value, 'r') as inputFile:
            code = inputFile.read()
    except Exception as e:
        raise schemeExceptions.SchemeException(e)
    code = "(begin {0} )".format(code)
    stream = SchemeStringStream(code)
    result = reader.SchemeReader().read(stream)
    result = evaluator.SchemeEvaluator().evaluate(result)
    return result

def builtin_printcwd(evaluatedArgs):
    if len(evaluatedArgs) != 0:
        raise schemeExceptions.ArgumentCountException('print-cwd expects no argument.')
    return SchemeString(os.getcwd())


# Syntax

def evaluate(arg, env):
    return evaluator.SchemeEvaluator().evaluate(arg, env)           # SchemeEvaluator is singleton


def builtin_and(unevaluatedArgs, env):
    for arg in unevaluatedArgs:
        condition = evaluate(arg, env)
        if(condition.isFalse()):
            return SchemeFalse()
    return SchemeTrue()

def builtin_or(unevaluatedArgs, env):
    for arg in unevaluatedArgs:
        condition = evaluate(arg, env)
        if(condition.isTrue()):
            return SchemeTrue()
    return SchemeFalse()

def builtin_begin(unevaluatedArgs, env):
    retVal = SchemeVoid()
    for arg in unevaluatedArgs:
        retVal = evaluate(arg, env)
    return retVal

def builtin_define(unevaluatedArgs, env):
    if len(unevaluatedArgs) < 2:
        raise schemeExceptions.ArgumentCountException('define expects at least 2 arguments.')

    if unevaluatedArgs[0].type == 'schemeCons':
        symbol = unevaluatedArgs[0].car
        lambdaArgs = unevaluatedArgs[0].cdr
        lambdaBody = unevaluatedArgs[1:]
        args = []
        args.append(lambdaArgs)
        args.extend(lambdaBody)
        evaluatedValue = builtin_lambda(args, env)
    else:
        if len(unevaluatedArgs) != 2:
            raise schemeExceptions.ArgumentCountException('define expects at exactly 2 arguments if no lambda short hand syntax is used.')
        symbol = unevaluatedArgs[0]
        unevaluatedValue = unevaluatedArgs[1]
        evaluatedValue = evaluate(unevaluatedValue, env)

    if symbol.type != 'schemeSymbol':
        raise schemeExceptions.ArgumentTypeException('define expects schemeSymbol as first argument.')

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
    success = env.setBinding(symbol, evaluate(unevaluatedArgs[1], env))
    if not success:
        raise schemeExceptions.NoBindingException('No binding found for symbol {0}.'.format(symbol))
    return SchemeVoid()

def builtin_let(unevaluatedArgs, env):
    pass

def builtin_quote(unevaluatedArgs, env):
    if len(unevaluatedArgs) != 1:
        raise schemeExceptions.ArgumentCountException('quote expects exactly 1 argument.')
    return unevaluatedArgs[0]





def initializeBindings():
    # add builtins to environments
    syntaxEnv = evaluator.SchemeEvaluator.syntaxEnv
    syntaxEnv.addBinding(SchemeSymbol('exit'), SchemeBuiltinFunction('exit', builtin_exit))
    syntaxEnv.addBinding(SchemeSymbol('if'), SchemeBuiltinSyntax('if', builtin_if))
    syntaxEnv.addBinding(SchemeSymbol('lambda'), SchemeBuiltinSyntax('lambda', builtin_lambda))
    syntaxEnv.addBinding(SchemeSymbol('define'), SchemeBuiltinSyntax('define', builtin_define))
    syntaxEnv.addBinding(SchemeSymbol('set!'), SchemeBuiltinSyntax('set!', builtin_set))
    syntaxEnv.addBinding(SchemeSymbol('let'), SchemeBuiltinSyntax('let', builtin_let))
    syntaxEnv.addBinding(SchemeSymbol('quote'), SchemeBuiltinSyntax('quote', builtin_quote))
    syntaxEnv.addBinding(SchemeSymbol('begin'), SchemeBuiltinSyntax('begin', builtin_begin))
    syntaxEnv.addBinding(SchemeSymbol('and'), SchemeBuiltinSyntax('and', builtin_and))
    syntaxEnv.addBinding(SchemeSymbol('or'), SchemeBuiltinSyntax('or', builtin_or))

    globalEnv = evaluator.SchemeEvaluator.globalEnv
    globalEnv.addBinding(SchemeSymbol('+'), SchemeBuiltinFunction('add', builtin_add))
    globalEnv.addBinding(SchemeSymbol('-'), SchemeBuiltinFunction('sub', builtin_sub))
    globalEnv.addBinding(SchemeSymbol('*'), SchemeBuiltinFunction('mul', builtin_mul))
    globalEnv.addBinding(SchemeSymbol('/'), SchemeBuiltinFunction('div', builtin_div))
    globalEnv.addBinding(SchemeSymbol('%'), SchemeBuiltinFunction('%', builtin_modulo))
    globalEnv.addBinding(SchemeSymbol('>'), SchemeBuiltinFunction('gt', builtin_gt))
    globalEnv.addBinding(SchemeSymbol('>='), SchemeBuiltinFunction('geqt', builtin_geqt))
    globalEnv.addBinding(SchemeSymbol('<'), SchemeBuiltinFunction('lt', builtin_lt))
    globalEnv.addBinding(SchemeSymbol('<='), SchemeBuiltinFunction('leqt', builtin_leqt))
    globalEnv.addBinding(SchemeSymbol('eq?'), SchemeBuiltinFunction('eq', builtin_eq))
    globalEnv.addBinding(SchemeSymbol('='), SchemeBuiltinFunction('eq_arit', builtin_eq_arit))
    globalEnv.addBinding(SchemeSymbol('abs'), SchemeBuiltinFunction('abs', builtin_abs))
    globalEnv.addBinding(SchemeSymbol('print'), SchemeBuiltinFunction('print', builtin_print))
    globalEnv.addBinding(SchemeSymbol('display'), SchemeBuiltinFunction('display', builtin_display))
    globalEnv.addBinding(SchemeSymbol('cons'), SchemeBuiltinFunction('cons', builtin_cons))
    globalEnv.addBinding(SchemeSymbol('car'), SchemeBuiltinFunction('car', builtin_car))
    globalEnv.addBinding(SchemeSymbol('cdr'), SchemeBuiltinFunction('cdr', builtin_cdr))
    globalEnv.addBinding(SchemeSymbol('first'), SchemeBuiltinFunction('first', builtin_first))
    globalEnv.addBinding(SchemeSymbol('rest'), SchemeBuiltinFunction('rest', builtin_rest))
    globalEnv.addBinding(SchemeSymbol('list'), SchemeBuiltinFunction('list', builtin_list))
    globalEnv.addBinding(SchemeSymbol('time'), SchemeBuiltinFunction('time', builtin_time))
    globalEnv.addBinding(SchemeSymbol('recursion-limit'), SchemeBuiltinFunction('recursion-limit', builtin_recursionlimit))
    globalEnv.addBinding(SchemeSymbol('type?'), SchemeBuiltinFunction('type?', builtin_type))
    globalEnv.addBinding(SchemeSymbol('list?'), SchemeBuiltinFunction('list?', builtin_isList))
    globalEnv.addBinding(SchemeSymbol('not'), SchemeBuiltinFunction('not', builtin_not))
    globalEnv.addBinding(SchemeSymbol('map'), SchemeBuiltinFunction('map', builtin_map))
    globalEnv.addBinding(SchemeSymbol('get-function-info'), SchemeBuiltinFunction('get-function-info', builtin_getfunctioninfo))
    globalEnv.addBinding(SchemeSymbol('eval-file'), SchemeBuiltinFunction('eval-file', builtin_evalfile))
    globalEnv.addBinding(SchemeSymbol('print-cwd'), SchemeBuiltinFunction('print-cwd', builtin_printcwd))



    globalEnv.addBinding(SchemeSymbol('nil'), SchemeNil())
    globalEnv.addBinding(SchemeSymbol('#f'), SchemeFalse())
    globalEnv.addBinding(SchemeSymbol('#t'), SchemeTrue())