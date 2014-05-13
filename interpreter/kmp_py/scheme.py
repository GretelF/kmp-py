from interpreter.kmp_py.schemeExceptions import *

class SchemeObject:
    def __init__(self):
        self.type = 'schemeObject'
        self.value = None

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __repr__(self):
        return "<{type}: {value}>".format(type=self.type, value=self.value)


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


class SchemeCons(SchemeObject):
    def __init__(self, car, cdr):
        super().__init__()
        self.car = car
        self.cdr = cdr
        self.type = 'schemeCons'

    def __eq__(self, other):
        return self.type == other.type and self.car == other.car and self.cdr == other.cdr

    def __str__(self):
        return '({car} . {cdr})'.format(car=str(self.car), cdr=str(self.cdr))


class SchemeNumber(SchemeObject):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.type = 'schemeNumber'

    def __str__(self):
        return '{0}'.format(self.value)

    def __add__(self, other):
        return SchemeNumber(self.value + other.value)

    def __mul__(self, other):
        return SchemeNumber(self.value * other.value)


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


class SchemeUserDefinedFunction(SchemeObject):
    def __init__(self, name, arglist, body, env):
        super().__init__()
        self.name = name
        self.arglist = arglist
        self.body = body
        self.env = env
        self.type = 'schemeUserDefinedFunction'


class SchemeBuiltinFunction(SchemeObject):
    def __init__(self, name, code):
        super().__init__()
        self.name = name
        self.code = code
        self.type = 'schemeBuiltinFunction'


class SchemeBuiltinSyntax(SchemeObject):
    def __init__(self, code):
        super().__init__()
        self.code = code
        self.type = 'schemeBuiltinSyntax'


class SchemeStringStream(SchemeObject):
    separatorList = {' ', '\n', '\t', '\r'}

    def __init__(self, inString):
        self.cursorPos = 0
        self.inString = inString

    def next(self, relAmount=1):
        if(not self.isAtEndOfStream()):
            self.cursorPos += 1

    def peek(self):
        return self.inString[self.cursorPos]

    def isAtEndOfStream(self):
        return (self.cursorPos > len(self.inString) - 1)

    def skipSeparators(self):
        while (self.peek() in self.separatorList):
            self.next()

    def seek(self, absAmount):
        if(absAmount >= len(self.inString) ):
            absAmount = len(self.inString) - 1
        elif(absAmount < -len(self.inString)):
            absAmount = -len(self.inString)

        amount = absAmount % len(self.inString)

        self.cursorPos = amount

class SchemeEnvironment(SchemeObject):
    def __init__(self):
        self.bindings = {}

    def addBinding(self, symbol, object):
        if(symbol.type != 'SchemeSymbol'):          # check if symbol is actually a schemeSymbol
            pass                                    # TODO: what to do here?

        if(symbol.value in self.bindings):
            pass                                    # TODO: raise exception???
        else:
            self.bindings[symbol.value] = object

    def getBinding(self, symbol):
        if(symbol.type != 'SchemeSymbol'):          # check if symbol is actually a schemeSymbol
            pass                                    # TODO: what to do here?

        if(symbol.value in self.bindings):
            return self.bindings[symbol.value]
        else:
            return None                             # TODO: what should be returned here?

    def setBinding(self, symbol, object):           # TODO: is this needed?
        if(symbol.type != 'SchemeSymbol'):          # check if symbol is actually a schemeSymbol
            pass                                    # TODO: what to do here?

        if(symbol.value in self.bindings):
            self.bindings[symbol.value] = object
        else:
            pass                                    # TODO: what to do here?


