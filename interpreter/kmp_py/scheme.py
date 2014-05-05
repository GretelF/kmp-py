

class schemeObject:
    def __eq__(self, other):
        return self.type == other.type and self.value == other.value



class schemeSingleton(schemeObject):
    _instance = None
    def __new__(singleton,*args,**kwargs):
        if not singleton._instance:
            singleton._instance = super(schemeSingleton, singleton).__new__(singleton, *args, **kwargs)
        return singleton._instance

class schemeFalse(schemeSingleton):
    def __init__(self):
        self.type = 'schemeFalse'

class schemeTrue(schemeSingleton):
    def __init__(self):
        self.type = 'schemeTrue'

class schemeCons(schemeObject):
    def __init__(self,car,cdr):
        self.car = car
        self.cdr = cdr
        self.type = 'schemeCons'

    def __eq__(self,other):
        return self.type == other.type and self.car == other.car and self.cdr == other.cdr

class schemeInteger(schemeObject):
    def __init__(self,value):
        self.value = value
        self.type = 'schemeInteger'

class schemeFloat(schemeObject):
    def __init__(self,value):
        self.value = value
        self.type = 'schemeFloat'

class schemeString(schemeObject):
    def __init__(self,value):
        self.value = value
        self.type = 'schemeString'

class schemeSymbol(schemeObject):
    def __init__(self,value):
        self.value = value
        self.type = 'schemeSymbol'

class schemeUserDefinedFunction(schemeObject):
    def __init__(self, arglist, body, env):
        self.arglist = arglist
        self.body = body
        self.env = env
        self.type = 'schemeUserDefinedFunction'

class schemeBuiltinFunction(schemeObject):
    def __init__(self,code):
        self.code = code
        self.type = 'schemeBuiltinFunction'

class schemeBuiltinSyntax(schemeObject):
    def __init__(self, code):
        self.code = code
        self.type = 'schemeBuiltinSyntax'




