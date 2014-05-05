

class schemeObject:
    def __eq__(self, other):
        return self.type == other.type and self.value == other.value
    def __repr__(self):
        return "<%s: %s>" % (self.type, self.value)

class schemeSingleton(schemeObject):
    _instance = None
    def __new__(singleton,*args,**kwargs):
        if not singleton._instance:
            singleton._instance = super(schemeSingleton, singleton).__new__(singleton, *args, **kwargs)
        return singleton._instance


class schemeFalse(schemeSingleton):
    def __init__(self):
        self.type = 'schemeFalse'
        self.value = 'False'

    def __str__(self):
        return '#f'


class schemeTrue(schemeSingleton):
    def __init__(self):
        self.type = 'schemeTrue'
        self.value = 'True'

    def __str__(self):
        return '#t'


class schemeNil(schemeSingleton):
    def __init__(self):
        self.type = 'schemeNil'
        self.value = None

    def __str__(self):
        return '()'

class schemeCons(schemeObject):
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr
        self.type = 'schemeCons'

    def __eq__(self,other):
        return self.type == other.type and self.car == other.car and self.cdr == other.cdr


class schemeNumber(schemeObject):
    def __init__(self, value):
        self.value = value
        self.type = 'schemeNumber'

    def __str__(self):
        return '%s' % self.value


class schemeString(schemeObject):
    def __init__(self, value):
        self.value = value
        self.type = 'schemeString'

    def __str__(self):
        return '%s' % self.value


class schemeSymbol(schemeObject):
    def __init__(self, value):
        self.value = value
        self.type = 'schemeSymbol'

    def __str__(self):
        return '%s' % self.value


class schemeUserDefinedFunction(schemeObject):
    def __init__(self, name, arglist, body, env):
        self.name = name
        self.arglist = arglist
        self.body = body
        self.env = env
        self.type = 'schemeUserDefinedFunction'


class schemeBuiltinFunction(schemeObject):
    def __init__(self, name, code):
        self.code = code
        self.type = 'schemeBuiltinFunction'



class schemeBuiltinSyntax(schemeObject):
    def __init__(self, code):
        self.code = code
        self.type = 'schemeBuiltinSyntax'




