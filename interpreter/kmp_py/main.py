from interpreter.kmp_py import reader, evaluator, scheme, initialize

def repl():
    initialize.initialize()
    e = evaluator.SchemeEvaluator()
    r = reader.SchemeReader()

    while True:
        print('> ', end='')
        toRead = input()
        stream = scheme.SchemeStringStream(toRead)
        while not stream.isAtEndOfStream():
            toEval = r.read(stream)
            toPrint = e.evaluate(toEval)
            if toPrint.type == 'schemeVoid':
                continue
            print(toPrint)




def main():
    repl()

if __name__ == '__main__':
    main()

