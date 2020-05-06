import tracing.exp as exp


def serverless_function(trace, args):

    def double_absolute_value(x):
        x000 = trace.trace_function_body('ret00')
        trace.trace_let('x', x000)
        trace.trace_let('double_x', 
        exp.UndefinedExp())
        double_x = None
        trace.trace_let('return_value', 
        exp.UndefinedExp())
        return_value = None
        trace.trace_set('double_x', 
        exp.BinaryOpExp('*', 
        exp.NumberExp(2), 
        exp.IdExp('x')))
        double_x = 2 * x
        test =  \
        exp.BinaryOpExp('<', 
        exp.IdExp('x'), 
        exp.NumberExp(0))
        if x < 0:
            trace.trace_if_true(test)
            trace.trace_set('return_value', 
            exp.UnaryOpExp('-', 
            exp.IdExp('double_x')))
            return_value = -double_x
        else:
            trace.trace_if_false(test)
            trace.trace_set('return_value', 
            exp.IdExp('double_x'))
            return_value = double_x
        trace.trace_break('ret00', 
        exp.IdExp('return_value'))
        trace.exit_block()
        return return_value
    trace.trace_function_call('result', [
    exp.IdExp('double_absolute_value'), 
    exp.IndexExp(
    exp.IdExp('args'), 
    exp.NumberExp(0))])
    result = double_absolute_value(args[0])
    return result