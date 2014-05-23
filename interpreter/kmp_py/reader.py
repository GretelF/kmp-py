from interpreter.kmp_py import scheme, schemeExceptions

class SchemeReader():
    def __init__(self):
        pass

    def _isSeparator(self, ch):
            return (type(ch) is str and ch in ' \n\t\r\v\f\b')

    def read(self, stream):
        stream.skipSeparators()
        ch = stream.peek()
        if(ch == '"'):
            return self.readString(stream)
        if(ch == ')'):
            raise schemeExceptions.InvalidInputException("unexpected ')'")
        if(ch == '('):
            return self.readList(stream)
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

        return scheme.SchemeString(s)

    def readAtom(self, stream):
        buffer = ''
        s = stream.peek()
        while(not stream.isAtEndOfStream() and not self._isSeparator(s) and s != '('  and s != ')'):
            buffer += s
            stream.next()
            s = stream.peek()
        if(buffer.isdigit() or (buffer[0]=='-' and buffer[1:].isdigit())):              # reads positive or negative number
            return scheme.SchemeNumber(int(buffer))
        else:
            return scheme.SchemeSymbol(buffer)

    def readList(self, stream):

        def helper(stream):
            stream.skipSeparators()
            s = stream.peek()
            if(s == ')'):
                stream.next()
                return scheme.SchemeNil()
            car = self.read(stream)
            cdr = helper(stream)
            return scheme.SchemeCons(car, cdr)



        stream.skipSeparators()
        s = stream.peek()

        if(s != '('):
            schemeExceptions.InvalidInputException('readList expects "(" as first character of stream')

        stream.next()
        buffer = helper(stream)

        return buffer




