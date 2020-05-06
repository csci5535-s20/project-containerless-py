import tracing.exp as exp


def serverless_function(trace, args):

    def ifelse():
        trace.trace_function_body('ret00')
        trace.trace_let('return_value', 
        exp.UndefinedExp())
        return_value = None
        trace.trace_set('return_value', 
        exp.NumberExp(1))
        return_value = 1
        test =  \
        exp.BinaryOpExp('==', 
        exp.NumberExp(24), 
        exp.NumberExp(42))
        if 24 == 42:
            trace.trace_if_true(test)
            trace.trace_set('return_value', 
            exp.NumberExp(0))
            return_value = 0
        else:
            trace.trace_if_false(test)
            trace.trace_set('return_value', 
            exp.NumberExp(2))
            return_value = 2
        trace.trace_break('ret00', 
        exp.IdExp('return_value'))
        trace.exit_block()
        return return_value
    trace.trace_function_call('result', [
    exp.IdExp('ifelse')])
    result = ifelse()
    return result