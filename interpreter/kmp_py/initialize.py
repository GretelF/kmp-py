from interpreter.kmp_py import scheme, evaluator, schemeBuiltin

# initializes (and therefore resets) the global environments syntaxEnv and globalEnv and initializes the builtin bindings.
def initialize():
    evaluator.SchemeEvaluator.syntaxEnv = scheme.SchemeEnvironment()
    evaluator.SchemeEvaluator.globalEnv = scheme.SchemeEnvironment()
    evaluator.SchemeEvaluator.globalEnv.parent = evaluator.SchemeEvaluator.syntaxEnv
    schemeBuiltin.initializeBindings()
