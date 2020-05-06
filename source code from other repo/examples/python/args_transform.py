import tracing.exp as exp


def serverless_function(trace, args):

    def echo(arg):
        arg000 = trace.trace_function_body('ret00')
        trace.trace_let('arg', arg000)
        trace.trace_break('ret00', 
        exp.IdExp('arg'))
        trace.exit_block()
        return arg
    trace.trace_function_call('result', [
    exp.IdExp('echo'), 
    exp.IndexExp(
    exp.IdExp('args'), 
    exp.NumberExp(0))])
    result = echo(args[0])
    return result