from interpreter.kmp_py import reader, evaluator, scheme, initialize, schemeExceptions

def repl():
    initialize.initialize()
    e = evaluator.SchemeEvaluator()
    r = reader.SchemeReader()

    while True:
        try:
            print('> ', end='')
            toRead = input()
            stream = scheme.SchemeStringStream(toRead)
            while not stream.isAtEndOfStream():
                toEval = r.read(stream)
                toPrint = e.evaluate(toEval)
                if toPrint.type == 'schemeVoid':
                    continue
                print(toPrint)
        except schemeExceptions.SchemeException as exception:
            print('{0}: {1}'.format(type(exception).__name__, exception))
        except Exception as exception:
            print('Critical error: {0}'.format(exception))





def main():
    repl()

if __name__ == '__main__':
    main()

