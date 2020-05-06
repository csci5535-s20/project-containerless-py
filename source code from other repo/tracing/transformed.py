import tracing.exp as exp


def serverless_function(trace, args):

    def arithmetic():
        trace.trace_function_body('ret00')
        trace.trace_let('foo', exp.UndefinedExp())
        foo = None
        trace.trace_let('bar', exp.UndefinedExp())
        bar = None
        trace.trace_let('res', exp.UndefinedExp())
        res = None
        trace.trace_set('foo', exp.NumberExp(2))
        foo = 2
        trace.trace_set('bar', exp.BinaryOpExp('+', exp.IdExp('foo'), exp.NumberExp(3)))
        bar = foo + 3
        trace.trace_set('res', exp.BinaryOpExp('*', exp.IdExp('foo'), exp.IdExp('bar')))
        res = foo * bar
        trace.trace_break('ret00', exp.IdExp('res'))
        trace.exit_block()
        return res

    trace.trace_function_call('result', [exp.IdExp('arithmetic'), args])
    result = arithmetic()

