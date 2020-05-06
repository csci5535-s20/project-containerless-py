from abc import ABCMeta, abstractmethod


class TracingException(Exception):
    pass


class TraceCompleteException(Exception):
    pass


class Cursor:
    def __init__(self, body):
        self.body = body
        self.index = 0

    def get_type(self):
        return type(self.body[self.index])

    def __repr__(self):
        return "Cursor({}, {})".format(self.body, self.index)


class TracerInterface(metaclass=ABCMeta):
    """
    This class corresponds to the TracingInterface interface in containerless.
    https://github.com/plasma-umass/decontainerization/blob/master/javascript/containerless/ts/types.ts
    """

    @abstractmethod
    def push_args(self, exps):
        """
        :param exps: Exp[]
        :return: None
        """

    @abstractmethod
    def pop_args(self):
        """
        :return: Exp[]
        """

    @abstractmethod
    def get_trace(self):
        """
        :return: Exp
        """

    @abstractmethod
    def new_trace(self):
        """
        :return: None
        """

    @abstractmethod
    def exit_block(self):
        """
        :return: None
        """

    @abstractmethod
    def trace_named(self, name):
        """
        :param name: str
        :return: None
        """

    @abstractmethod
    def trace_let(self, name, named):
        """
        :param name: str
        :param named: Exp
        :return: None
        """

    @abstractmethod
    def trace_function_call(self, name, args):
        """
        :param name: str
        :param args: Exp[]
        :return: None
        """

    @abstractmethod
    def trace_function_body(self, label_name):
        """
        :param label_name: str
        :return: Exp[]
        """

    @abstractmethod
    def trace_set(self, name, named):
        """
        :param name: LVal
        :param named: Exp
        :return: None
        """

    @abstractmethod
    def trace_if_true(self, condition):
        """
        :param condition: Exp
        :return: None
        """

    @abstractmethod
    def trace_if_false(self, condition):
        """
        :param condition: Exp
        :return: None
        """

    @abstractmethod
    def trace_while(self, condition):
        """
        :param condition: Exp
        :return: None
        """

    @abstractmethod
    def trace_loop(self):
        """
        :return: None
        """

    @abstractmethod
    def trace_callback(self, event, event_arg, callback_args, clos):
        """
        :param event: str
        :param event_arg: Exp
        :param callback_args: str[]
        :param clos: Exp
        :return: Tracer
        """

    @abstractmethod
    def trace_prim_app(self, event, event_args):
        """
        :param event: str
        :param event_args: Exp[]
        :return: None
        """

    @abstractmethod
    def trace_break(self, name, value):
        """
        :param name: str
        :param value: Exp
        :return: None
        """

    @abstractmethod
    def trace_label(self, name):
        """
        :param name: str
        :return: None
        """

    @abstractmethod
    def trace_return(self, exp):
        """
        :param exp: Exp
        :return: None
        """

    @abstractmethod
    def get_trace_json(self):
        """
        :return: None
        """
