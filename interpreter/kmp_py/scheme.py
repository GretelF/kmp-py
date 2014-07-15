from interpreter.kmp_py.schemeExceptions import *

class SchemeObject:
    def __init__(self):
        self.type = 'schemeObject'
        self.value = None

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __repr__(self):
        return "<{type}: {value}>".format(type=self.type, value=self.value)

    def isTrue(self):
        return True

    def isFalse(self):
        return False

class SchemeSingleton(SchemeObject):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SchemeSingleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class SchemeFalse(SchemeSingleton):
    def __init__(self):
        super().__init__()
        self.type = 'schemeFalse'
        self.value = 'False'

    def __str__(self):
        return '#f'

    def isTrue(self):
        return False

    def isFalse(self):
        return True


class SchemeTrue(SchemeSingleton):
    def __init__(self):
        super().__init__()
        self.type = 'schemeTrue'
        self.value = 'True'

    def __str__(self):
        return '#t'


class SchemeNil(SchemeSingleton):
    def __init__(self):
        super().__init__()
        self.type = 'schemeNil'
        self.value = None

    def __str__(self):
        return '()'


class SchemeVoid(SchemeSingleton):
    def __init__(self):
        super().__init__()
        self.type = 'schemeVoid'
        self.value = None

    def __str__(self):
        return ''


class SchemeCons(SchemeObject):
    def __init__(self, car, cdr):
        super().__init__()
        self.car = car
        self.cdr = cdr
        self.type = 'schemeCons'

    def __eq__(self, other):
        return self is other

    def __str__(self):
        buffer = '('
        buffer = buffer + self.__strHelper()
        buffer = buffer + ')'
        return buffer

    def __strHelper(self):
        buffer = ''
        buffer = buffer + str(self.car)
        if (self.cdr.type == 'schemeCons'):
            buffer = buffer + ' ' + self.cdr.__strHelper()
        elif (self.cdr.type != 'schemeNil'):
            buffer = buffer + ' . ' + str(self.cdr)
        return buffer

    def toArray(self):
        array = []
        car = self.car
        array.append(car)
        cdr = self.cdr
        if cdr.type == 'schemeNil':
            return array
        if cdr.type != 'schemeCons':
            array.append(cdr)
            return tuple(array)
        array.extend(cdr.toArray())
        return array


class SchemeNumber(SchemeObject):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.type = 'schemeNumber'

    def __str__(self):
        return '{0}'.format(self.value)


class SchemeString(SchemeObject):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.type = 'schemeString'

    def __str__(self):
        return '"{0}"'.format(self.value)


class SchemeSymbol(SchemeObject):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.type = 'schemeSymbol'

    def __str__(self):
        return '{0}'.format(self.value)

    _schemeSymbolList = dict()

    def __new__(cls, val):
        if not val in cls._schemeSymbolList.keys():
            cls._schemeSymbolList[val] = SchemeObject.__new__(cls)
        return cls._schemeSymbolList[val]


class SchemeUserDefinedFunction(SchemeObject):
    def __init__(self, name, arglist, body, env):
        super().__init__()
        self.name = name
        self.arglist = arglist
        self.body = body
        self.env = env
        self.type = 'schemeUserDefinedFunction'


class SchemeBuiltinFunction(SchemeObject):
    def __init__(self, name, func):
        super().__init__()
        self.name = name
        self.func = func
        self.type = 'schemeBuiltinFunction'


class SchemeBuiltinSyntax(SchemeObject):
    def __init__(self, name, func):
        super().__init__()
        self.name = name
        self.func = func
        self.type = 'schemeBuiltinSyntax'


class SchemeStringStream(SchemeObject):
    separatorList = {' ', '\n', '\t', '\r', '\f', '\v', '\b'}

    def __init__(self, inString):
        super().__init__()
        self.cursorPos = 0
        self.inString = inString

    def next(self, relAmount=1):
        if(not self.isAtEndOfStream()):
            self.cursorPos += 1

    def peek(self):
        if(self.isAtEndOfStream()):
            return None
        return self.inString[self.cursorPos]

    def isAtEndOfStream(self):
        return (self.cursorPos > len(self.inString) - 1)

    def skipSeparators(self):
        while (not self.isAtEndOfStream() and self.peek() in self.separatorList):
            self.next()

    def seek(self, absAmount):
        if(absAmount >= len(self.inString) ):
            absAmount = len(self.inString) - 1
        elif(absAmount < -len(self.inString)):
            absAmount = -len(self.inString)

        amount = absAmount % len(self.inString)

        self.cursorPos = amount

class SchemeEnvironment(SchemeObject):
    def __init__(self, parent = None):
        super().__init__()
        self.bindings = {}
        self.parent = parent

    def __eq__(self, other):
        return self is other


    def addBinding(self, symbol, object):           # used for LISP function define
        if(symbol.type != 'schemeSymbol'):          # check if symbol is actually a schemeSymbol
            raise InvalidInputException("function addBinding requests SchemeSymbol")

        if(symbol.value in self.bindings):
            return None
        else:
            self.bindings[symbol.value] = object

    def getBinding(self, symbol):
        if(symbol.type != 'schemeSymbol'):          # check if symbol is actually a schemeSymbol
            raise InvalidInputException("function addBinding requests SchemeSymbol")

        if(symbol.value in self.bindings):
            return self.bindings[symbol.value]
        elif(self.parent != None):
            return self.parent.getBinding(symbol)
        else:
            return None                             # TODO: what should be returned in case, no binding is found at all? None? Error?

    def setBinding(self, symbol, object):           # used for LISP function set!
        if(symbol.type != 'schemeSymbol'):          # check if symbol is actually a schemeSymbol
            raise InvalidInputException("function addBinding requests SchemeSymbol")

        if(symbol.value in self.bindings):
            self.bindings[symbol.value] = object
        else:
            return None                             # TODO: what should be returned in case, no binding is found at all? None? Error?

    def __str__(self):
        buffer = "<environment:\n"
        for binding in self.bindings:
            buffer = buffer + str(binding) + " = " + str(self.bindings[binding]) + "\n"
        buffer = buffer + ">"
        return buffer
