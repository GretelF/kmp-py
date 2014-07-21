
class SchemeException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)

class EOFException(SchemeException):
    pass

class InvalidInputException(SchemeException):
    pass

class NoBindingException(SchemeException):
    pass

class ArgumentCountException(InvalidInputException):
    pass

class ArgumentTypeException(InvalidInputException):
    pass

class DivisionByZero(InvalidInputException):
    pass

