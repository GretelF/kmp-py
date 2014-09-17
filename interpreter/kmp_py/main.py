from interpreter.kmp_py import reader, evaluator, scheme, initialize, schemeExceptions

def repl():
    initialize.initialize()
    e = evaluator.SchemeEvaluator()
    r = reader.SchemeReader()

    initCode = ''
    with open('init.lisp', 'r') as initfile:
        initCode = initfile.read()
    initCode = "(begin {0} )".format(initCode)
    stream = scheme.SchemeStringStream(initCode)
    initEval = r.read(stream)
    initPrint = e.evaluate(initEval)
    if initPrint.type != 'schemeVoid':
        print(initPrint)

    while True:
        try:
            toRead = input('> ')
            stream = scheme.SchemeStringStream(toRead)
            syntaxResult = r.checkSyntax(stream)
            while not syntaxResult.isBalanced() and syntaxResult.isValid():
                toRead += "\n" + input()
                stream = scheme.SchemeStringStream(toRead)
                syntaxResult = r.checkSyntax(stream)
            while not stream.isAtEndOfStream():
                toEval = r.read(stream)
                toPrint = e.evaluate(toEval)
                if toPrint.type != 'schemeVoid':
                    print(toPrint)
        except schemeExceptions.SchemeException as exception:
            print('{0}: {1}'.format(type(exception).__name__, exception))
        except Exception as exception:
            print('Critical error: {0}'.format(exception))





def main():
    repl()

if __name__ == '__main__':
    main()

