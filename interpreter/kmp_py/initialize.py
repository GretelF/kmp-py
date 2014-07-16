from interpreter.kmp_py import evaluator, schemeBuiltin
from interpreter.kmp_py.scheme import SchemeEnvironment

# initializes (and therefore resets) the global environments syntaxEnv and globalEnv and initializes the builtin bindings.
def initialize():
    evaluator.SchemeEvaluator.syntaxEnv = SchemeEnvironment()
    evaluator.SchemeEvaluator.globalEnv = SchemeEnvironment()
    evaluator.SchemeEvaluator.globalEnv.parent = evaluator.SchemeEvaluator.syntaxEnv
    schemeBuiltin.initializeBindings()
