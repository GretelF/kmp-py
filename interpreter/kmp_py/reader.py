from interpreter.kmp_py import schemeExceptions
from interpreter.kmp_py.scheme import *

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

        return SchemeString(s)

    def readAtom(self, stream):
        buffer = ''
        s = stream.peek()
        while(not stream.isAtEndOfStream() and not self._isSeparator(s) and s != '('  and s != ')'):
            buffer += s
            stream.next()
            s = stream.peek()
        if(buffer.isdigit() or (buffer[0]=='-' and buffer[1:].isdigit())):              # reads positive or negative number
            return SchemeNumber(int(buffer))
        else:
            return SchemeSymbol(buffer)

    def readList(self, stream):

        def helper(stream):
            stream.skipSeparators()
            s = stream.peek()
            if(s == ')'):
                stream.next()
                return SchemeNil()
            car = self.read(stream)
            cdr = helper(stream)
            return SchemeCons(car, cdr)

        stream.skipSeparators()
        stream.next()
        buffer = helper(stream)

        return buffer




