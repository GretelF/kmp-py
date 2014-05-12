from interpreter.kmp_py import scheme, schemeExceptions

class SchemeReader():
    def __init__(self):
        pass

    def read(self, inString):
        stream = scheme.SchemeStringStream(inString)
        stream.skipSeparators()
        ch = stream.peek()
        if(ch == '"'):
            return self.readString(stream)

    def readString(self, stream):
        s = ''
        stream.next()

        while(True):
            if(stream.isAtEndOfStream()):
                raise schemeExceptions.EOFException('unexpected end of stream.')
            if(stream.peek() == '"'):
                stream.next()
                break
            s += stream.peek()
            stream.next()

        return scheme.SchemeString(s)
