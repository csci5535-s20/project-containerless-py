import tracing.exp as exp


def serverless_function(trace, args):

    def foo():
        trace.trace_function_body('ret00')
        trace.trace_let('ret_val', 
        exp.UndefinedExp())
        ret_val = None

        def bar():
            trace.trace_function_body('ret00')
            trace.trace_break('ret00', 
            exp.NumberExp(2))
            trace.exit_block()
            return 2
        trace.trace_function_call('ret_val', ['bar'])
        ret_val = bar()
        trace.trace_break('ret00', 
        exp.IdExp('ret_val'))
        trace.exit_block()
        return ret_val
    trace.trace_function_call('result', [
    exp.IdExp('foo')])
    result = foo()
    return result