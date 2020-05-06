from tracing.tracer_interface import TracerInterface, TracingException
from tracing.exp import UnknownExp


def create_trace(verbose=False):
    return MockTracer([UnknownExp()], verbose)


class MockTracer(TracerInterface):

    def __init__(self, body, verbose=False):
        pass

    def push_args(self, exps):
        pass

    def pop_args(self):
        return [UnknownExp(), UnknownExp(), UnknownExp(), UnknownExp(), UnknownExp()]

    def get_trace(self):
        return UnknownExp()

    def new_trace(self):
        pass

    def exit_block(self):
        pass

    def trace_named(self, name):
        pass

    def trace_let(self, name, named):
        pass

    def trace_function_call(self, name, args):
        pass

    def trace_function_body(self, label_name):
        return []

    def trace_set(self, name, named):
        pass

    def trace_if_true(self, condition):
        pass

    def trace_if_false(self, condition):
        pass

    def trace_while(self, condition):
        pass

    def trace_loop(self):
        pass

    def trace_callback(self, event, event_arg, callback_args, clos):
        return MockTracer([UnknownExp()])

    def trace_prim_app(self, event, event_args):
        pass

    def trace_break(self, name, value):
        raise TracingException("trace_break is not implemented.")

    def trace_label(self, name):
        pass

    def trace_return(self, exp):
        pass

    def get_trace_json(self):
        pass
