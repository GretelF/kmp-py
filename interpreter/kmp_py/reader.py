from interpreter.kmp_py import schemeExceptions
from interpreter.kmp_py.scheme import *
import copy

class SyntaxResult():
    def __init__(self):
        self.balance = 0
        self.valid = True

    def isBalanced(self):
        return self.balance == 0

    def isValid(self):
        return self.valid

class SchemeReader():
    def __init__(self):
        pass

    def _isSeparator(self, ch):
        return (type(ch) is str and ch in ' \n\t\r\v\f\b')

    def checkSyntax(self, stream):
        result = SyntaxResult()
        stream = copy.copy(stream)                 # checkSyntax should not alter index of the original stream object.
        while True:
            stream.skipSeparators()
            if stream.isAtEndOfStream():
                break
            c = stream.peek()
            if c == '(':
                result.balance += 1
            elif c == ')':
                result.balance -= 1
                if result.balance < 0:
                    result.valid = False
            stream.next()
        return result

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
        def isInteger(string):
            if string.startswith('-'):
                string = string[1:]
            return string.isdigit()

        def isFloat(string):
            try:
                float(string)
                return True
            except ValueError:
                return False

        buffer = ''
        s = stream.peek()
        while(not stream.isAtEndOfStream() and not self._isSeparator(s) and s != '('  and s != ')'):
            buffer += s
            stream.next()
            s = stream.peek()

        if isInteger(buffer):              # reads positive or negative number
            return SchemeNumber(int(buffer))
        if isFloat(buffer):
            return SchemeNumber(float(buffer))
        else:
            return SchemeSymbol(buffer)

    def readList(self, stream):

        def helper(stream):
            stream.skipSeparators()
            if stream.isAtEndOfStream():
                raise schemeExceptions.EOFException('unexpected end of stream while reading list.')
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




