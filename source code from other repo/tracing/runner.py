from tracing.tracer import create_trace
from tracing.mock_tracer import create_trace as create_mock_trace


def run_trace(serverless_function, arg=[], verbose=False, tracing=True):
    if tracing:
        tracer = create_trace(verbose)
    else:
        tracer = create_mock_trace(verbose)

    result = serverless_function(tracer, arg)
    return (result, tracer.get_trace_json())
