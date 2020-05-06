import logging

from tracing.tracer_interface import TracerInterface, Cursor, TraceCompleteException, TracingException
from tracing.exp import *

FORMAT = "[%(name)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)


def create_trace(verbose=False):
    return Tracer([UnknownExp()], verbose)


class Tracer(TracerInterface):

    def __init__(self, body, verbose=False):
        """
        :param body: BlockExp
        """
        self.trace = BlockExp(body)
        self.cursor_stack = []
        self.cursor = Cursor(body)
        self.args_buff = None
        self.logger = logging.getLogger('tracer')
        if verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.ERROR)
        self.logger.debug("body={}".format(body))

    def get_valid_cursor(self):
        """
        Private method checking the current cursor
        :return: cursor
        """
        if self.cursor is None:
            raise TraceCompleteException("Trace is Complete!")
        self.logger.debug("cursor={}".format(self.cursor))
        return self.cursor

    def get_current_exp(self):
        cursor = self.get_valid_cursor()
        if cursor.index is len(cursor.body):
            raise TracingException("Attempting to trace after the end of a block (cursor is {})".format(cursor))
        self.logger.debug("current_expression={}".format(cursor.body[cursor.index]))
        return cursor.body[cursor.index]

    def get_prev_exp(self):
        cursor = self.get_valid_cursor()
        if (cursor.index is 0) and (len(cursor.body) > 1):
            raise TracingException("No previous exp.")
        elif (cursor.index is 0) and (len(cursor.body) is 1):
            ''' (Comment from Containerless: If you call a function inside of a loop...
            The first time, there will be an unknown at the end of the body
            The next time, there will not be
            '''
            self.logger.debug("previous_expression={}".format(cursor.body[cursor.index]))
            return cursor.body[cursor.index]
        else:
            self.logger.debug("previous_expression={}".format(cursor.body[cursor.index - 1]))
            return cursor.body[cursor.index - 1]

    def can_increment_cursor(self):
        cursor = self.get_valid_cursor()
        if (cursor.index == len(cursor.body) - 1) and (cursor.get_type() is not UnknownExp):
            self.logger.debug("Cannot increment cursor")
            return
        self.logger.debug("Incremented cursor")
        cursor.index += 1

    def set_exp(self, exp):
        cursor = self.get_valid_cursor()

        if cursor.get_type() is not UnknownExp:
            raise TracingException("Cannot discard expression of type {}".format(cursor.get_type()))

        cursor.body[cursor.index] = exp
        cursor.body.append(UnknownExp())
        cursor.index += 1
        self.logger.debug("exp={}".format(exp))

    def enter_block(self, cursor):
        self.logger.debug("cursor={}".format(cursor))
        if self.cursor:
            self.cursor_stack.append(self.cursor)
        self.cursor = cursor

    # utility method
    def push_arg(self, exp):
        self.logger.debug("exp={}, args_buff={}".format(exp, self.args_buff))
        if self.args_buff is None:
            self.args_buff = exp
        else:
            raise TracingException("Already something in the args buffer.")

    def push_args(self, exps):
        self.logger.debug("")
        self.push_arg(ArrayExp(exps))

    # utility method
    def pop_arg(self):
        self.logger.debug("args_buff={}".format(self.args_buff))
        if self.args_buff:
            e = self.args_buff
            self.args_buff = None
            return e
        else:
            raise TracingException("Nothing in the args buffer.")

    def pop_args(self):
        self.logger.debug("")
        e = self.pop_arg()
        if not isinstance(e, ArrayExp):
            raise TracingException("Expected array type in args buffer")
        return e.exps

    def get_trace(self):
        self.logger.debug("")
        return self.trace

    def new_trace(self):
        self.logger.debug("")
        self.cursor = Cursor(self.trace.body)
        self.cursor_stack = []

    def exit_block(self):
        self.logger.debug("")
        if not self.cursor:
            raise TracingException("called exit_block on a complete trace")

        if len(self.cursor.body) is 0:
            # There is nothing in this block (e.g. empty else block)
            self.cursor = self.cursor_stack.pop()
        else:
            if self.cursor.index != len(self.cursor.body) - 1:
                raise TracingException("Exiting block too early")
            if isinstance(self.cursor.body[self.cursor.index], UnknownExp):
                self.cursor.body.pop()
            self.cursor = self.cursor_stack.pop()

    def exit_block_quiet(self):
        self.logger.debug("")
        if not self.cursor:
            raise TracingException("called exit_block on a complete trace")
        self.cursor = self.cursor_stack.pop()

    def trace_named(self, name):
        """
        (From containerless:
        Creates the trace expression 'let name = { unknown };' and enters the
        block containing the 'unknown'.)
        :param name:
        :return:
        """
        self.logger.debug("name={}".format(name))
        e = self.get_current_exp()
        if isinstance(e, UnknownExp):
            named_block = BlockExp([UnknownExp()])
            self.set_exp(LetExp(name, named_block))
            self.enter_block(Cursor(named_block.body))

        elif isinstance(e, LetExp):
            if e.name != name:
                raise TracingException("Cannot merge let with name {} into let with name {}".format(e.name, name))
            self.can_increment_cursor()
            if not isinstance(e.named, BlockExp):
                raise TracingException("Expected block on right hand side of let")
            self.enter_block(Cursor(e.named.body))
        else:
            raise TracingException("Expected let, got {}".format(type(e)))

    def trace_let(self, name, named):
        self.logger.debug("name={}, named={}".format(name, named))
        exp = self.get_current_exp()
        if isinstance(exp, UnknownExp):
            self.set_exp(LetExp(name, named))
        elif isinstance(exp, LetExp):
            if exp.name != name:
                raise TracingException("Cannot merge let with name {} into let with name {}".format(exp.name, name))
            exp.named.merge(named)
            self.can_increment_cursor()
        else:
            raise TracingException("Expected let, got {}".format(type(exp)))

    def trace_function_call(self, name, args):
        self.logger.debug("name={}, args={}".format(name, args))
        self.push_args(args)
        self.trace_named(name)

    def trace_function_body(self, label_name):
        self.logger.debug("label_name={}".format(label_name))
        self.trace_label(label_name)
        return self.pop_args()

    def trace_set(self, name, named):
        self.logger.debug("name={}, named={}".format(name, named))
        exp = self.get_current_exp()
        if isinstance(exp, UnknownExp):
            self.set_exp(SetExp(name, named))

        elif isinstance(exp, SetExp):
            exp.name.merge_exp(name)
            exp.named.merge_exp(named)
            self.can_increment_cursor()

        else:
            raise TracingException("Expected set, got {}".format(type(exp)))

    def trace_if_true(self, condition):
        self.logger.debug("condition={}".format(condition))
        exp = self.get_current_exp()
        if isinstance(exp, UnknownExp):
            new_block = [UnknownExp()]
            self.set_exp(IfExp(condition, new_block, [UnknownExp()]))
            self.enter_block(Cursor(new_block))
        elif isinstance(exp, IfExp):
            exp.condition.merge_exp(condition)
            self.can_increment_cursor()
            self.enter_block(Cursor([exp.true_part]))
        else:
            raise TracingException("Expected If, got {}".format(type(exp)))

    def trace_if_false(self, condition):
        self.logger.debug("condition={}".format(condition))
        exp = self.get_current_exp()
        if isinstance(exp, UnknownExp):
            new_block = [UnknownExp()]
            self.set_exp(IfExp(condition, [UnknownExp()], new_block))
            self.enter_block(Cursor(new_block))
        elif isinstance(exp, IfExp):
            exp.condition.merge_exp(condition)
            self.can_increment_cursor()
            self.enter_block(Cursor([exp.false_part]))
        else:
            raise TracingException("Expected If, got {}".format(type(exp)))

    def trace_while(self, condition):
        self.logger.debug("condition={}".format(condition))
        exp = self.get_current_exp()
        if isinstance(exp, UnknownExp):
            new_block = BlockExp([UnknownExp()])
            self.set_exp(WhileExp(condition, new_block))
            self.enter_block(Cursor([new_block]))
        elif isinstance(exp, WhileExp):
            exp.condition.merge_exp(condition)
            self.can_increment_cursor()
            self.enter_block(Cursor([exp.body]))
        else:
            raise TracingException("Expected While, got {}".format(type(exp)))

    def trace_loop(self):
        self.logger.debug("")
        cursor = self.get_valid_cursor()
        cursor.index = 0

    def trace_callback(self, event, event_arg, callback_args, clos):
        self.logger.debug("event={}, event_arg={}, callback_args={}, clos={}".format(
            event, event_arg, callback_args, clos))
        exp = self.get_current_exp()

        if isinstance(exp, UnknownExp):
            callback_body = [UnknownExp()]
            self.set_exp(CallbackExp(event, event_arg, callback_args, clos, callback_body))
            return Tracer(callback_body)

        elif isinstance(exp, CallbackExp):

            # Check event argument
            if (exp.event != event) or (len(exp.callback_args) != len(callback_args)):
                raise TracingException("Called trace_callback({}), but hole contains trace_callback({})".format(
                    event, exp.event))

            # Check callback_args argument
            for i in range(len(exp.callback_args)):
                if exp.callback_args[i] != callback_args[i]:
                    raise TracingException("Called trace_callback({}), but hole contains trace_callback({})".format(
                        event, exp.event))

            exp.clos.merge_exp(clos)
            exp.event_arg.merge_exp(event_arg)

            self.can_increment_cursor()
            return Tracer(exp.body)

        else:
            raise TracingException("hole contains {}".format(type(exp)))

    def trace_prim_app(self, event, event_args):
        self.logger.debug("event={}, event_args={}".format(event, event_args))
        exp = self.get_current_exp()

        if isinstance(exp, UnknownExp):
            self.set_exp(PrimAppExp(event, event_args))

        elif isinstance(exp, PrimAppExp):
            if exp.event != event:
                raise TracingException("Cannot merge event with name {} into let with name {}".format(event, exp.event))
            Exp.merge_exp_array(exp.event_args, event_args)
            self.can_increment_cursor()

        else:
            raise TracingException("Expected PrimAppExp, but {}".format(type(exp)))

    def trace_label(self, name):
        self.logger.debug("name={}".format(name))
        exp = self.get_current_exp()
        if isinstance(exp, UnknownExp):
            label_body = [UnknownExp()]
            self.set_exp(LabelExp(name, label_body))
            self.enter_block(Cursor(label_body))
        elif isinstance(exp, LabelExp):
            if exp.name != name:
                raise TracingException("Cannot merge label with name {} into label with  name {}".format(
                    name, exp.name))
            self.can_increment_cursor()
            self.enter_block(Cursor(exp.body))
        else:
            raise TracingException('expected LabelExp, got {}'.format(type(exp)))

    def trace_break(self, name, value):
        exp = self.get_current_exp()
        if isinstance(exp, UnknownExp):
            self.set_exp(BreakExp(name, value))
        elif isinstance(exp, BreakExp):
            if exp.name != name:
                raise TracingException('Cannot merge break with name {} into break with name {}'.format(name, exp.name))
            exp.value.merge_exp(value)
            self.can_increment_cursor()
        else:
            raise TracingException('expected break, got {}'.format(type(exp)))

        # Rewind
        # Keep exiting until you reach the correct label
        self.exit_block()
        prev = self.get_prev_exp()
        while (isinstance(prev, LabelExp) and prev.name != name) or (not isinstance(prev, LabelExp)):
            self.exit_block_quiet()
            prev = self.get_prev_exp()

        # Resume normal control flow.
        if not isinstance(prev, LabelExp):
            raise TracingException('Expected label!')

    def trace_return(self, exp):
        # Note(erika): Went ahead and modified this to support our new expressions.
        self.logger.debug("exp={}".format(exp))
        exp2 = self.get_current_exp()
        if isinstance(exp2, UnknownExp):
            self.set_exp(exp)
        else:
            exp2.merge(exp)

    def get_trace_json(self):
        # Note: changed separators to make json.dumps (Python) more analogous to JSON.stringify (JS)
        # per this source: https://stackoverflow.com/questions/46227854/json-stringify-javascript-and-json-dumps-
        # python-not-equivalent-on-a-list/46227888
        return json.dumps(self.get_trace(), separators=(',', ':'), default=lambda obj: obj.toJson())

