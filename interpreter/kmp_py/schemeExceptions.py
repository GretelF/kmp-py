
class SchemeException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class EOFException(SchemeException):
    pass

class InvalidInputException(SchemeException):
    pass

class NoBindingException(SchemeException):
    pass

class ArgumentCountException(SchemeException):
    pass

class ArgumentTypeException(SchemeException):
    pass

