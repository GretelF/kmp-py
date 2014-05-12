from interpreter.kmp_py import scheme, schemeExceptions

class SchemeReader():
    def __init__(self):
        pass

    def _isSeparator(self, ch):
        return (ch == ' ' or ch == '\t' or ch == '\n' or ch == '\r')

    def read(self, inString):
        stream = scheme.SchemeStringStream(inString)
        stream.skipSeparators()
        ch = stream.peek()
        if(ch == '"'):
            return self.readString(stream)
        if(ch == ')'):
            raise schemeExceptions.InvalidInputException("unexpected ')'")
        if(ch == '('):
            pass # return self.readList(stream)
        return self.readAtom(stream)

    def readString(self, stream):
        s = ''
        stream.next()                           # read over opening '"'

        while(True):
            if(stream.isAtEndOfStream()):
                raise schemeExceptions.EOFException('unexpected end of stream.')
            if(stream.peek() == '"'):
                stream.next()
                break
            s += stream.peek()
            stream.next()
        stream.next()                           # read over closing '"'

        return scheme.SchemeString(s)

    def readAtom(self, stream):
        buffer = ''
        s = stream.peek()
        while(True):
            if(self._isSeparator(s) or s == '('  or s == ')' or stream.isAtEndOfStream()):
                if(buffer.isdigit()):
                    return scheme.SchemeNumber(int(buffer))
                else:
                    return scheme.SchemeSymbol(buffer)
            else:
                buffer += stream.peek()
                stream.next()



