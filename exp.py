from abc import ABCMeta


class UnaryOperator:
    OPS = ['typeof', '-']

    def __init__(self, op):
        if op in BinaryOperator.OPS:
            self.op = op
        else:
            raise ValueError("Unknown Unary Operator: {}".format(op))


class BinaryOperator:
    OPS = ['+', '-', '*', '/', '==', '!=', '>', '<', '>=', '<=', '&&', '||']

    def __init__(self, op):
        if op in BinaryOperator.OPS:
            self.op = op
        else:
            raise ValueError("Unknown Binary Operator: {}".format(op))


class Exp(metaclass=ABCMeta):
    """
    This abstract class takes the place of the abstract datatype for expressions, Exp
    """
    pass


class LVal(Exp):
    """
    A subclass of Exp, used by IdExp, FromExp, IndexExp
    """
    pass


class BlockExp(Exp):
    def __init__(self, body):
        """
        :param body: a list of expressions, Exp[]
        """
        self.body = body


class LetExp(Exp):
    def __init__(self, name, exp):
        self.name = name
        self.exp = exp


class SetExp(Exp):
    def __init__(self, leftval, exp):
        self.leftval = leftval
        self.exp = exp


class IfExp(Exp):
    def __init__(self, condition, true_part, false_part):
        self.condition = condition
        self.true_part = true_part
        self.false_part = false_part


class WhileExp(Exp):
    def __init__(self, condition, body):
        """
        :param condition:
        :param body: A list of expressions
        """
        self.condition = condition
        self.body = body


class CallbackExp(Exp):
    """
    TODO(erika): I'm not sure if this should change for Python.
    """
    def __init__(self, event, event_arg, callback_args, clos, body):
        """
        :param event: string
        :param event_arg: Exp (argument for the event, e.g. the URL to get)
        :param callback_args: string[] (name of arguments passed to the callback)
        :param clos: Exp
        :param body: Exp[] (body of the callback)
        """
        self.event = event
        self.event_arg = event_arg
        self.callback_args = callback_args
        self.clos = clos
        self.body = body


class PrimAppExp(Exp):
    """
    TODO(erika): I'm not sure what this is.
    """
    def __init__(self, event, event_args):
        self.event = event
        self.event_args = event_args


class LabelExp(Exp):
    """
    TODO(erika): I'm not sure how labelled code plays into Python???
    """
    def __init__(self, name, body):
        """
        :param name: string (name of the label)
        :param body: Exp[]
        """
        self.name = name
        self.body = body


class BreakExp(Exp):
    def __init__(self, name, value):
        """
        :param name: string
        :param value: Exp
        """
        self.name = name
        self.value = value


class IdExp(LVal):
    """
    Class representing an identifier
    """
    def __init__(self, name):
        self.name = name


class FromExp(LVal):
    """
    Note from JS: "A FromExp reads a value out of a closure, thus needs to be derefenced
    TODO(erika): Not sure how this translates from Python
    """
    def __init__(self, exp, field):
        self.exp = exp
        self.field = field


def froms(clos, ids):
    """
    Helper function for created an array of FromExps. Analagous to froms() in the JS version.
    :param clos:
    :param ids:
    :return:
    """
    ret = []
    for id in ids:
        ret.append(FromExp(clos, id))
    return ret


class GetExp(Exp):
    """
    Note from JS: "A GetExp reads a value out of an object"
    """
    def __init__(self, exp, field):
        self.exp = exp
        self.field = field


''' TODO(erika): Not sure how/what I need TEnv for:
type TEnv = { [key: string]: Exp };

I think we can just use a python dictionary rather than defining
a whole new thing here.
'''


class ObjExp(Exp):
    def __init__(self, properties):
        """
        :param properties: TODO(erika) - tenv things
        """
        self.properties = properties


class ClosExp(Exp):
    def __init__(self, tenv):
        """
        TODO(erika): What exactly is TEnv doing?
        :param tenv:
        """
        self.tenv = tenv


class ArrayExp(Exp):
    def __init__(self, exps):
        """
        :param properties: tenv (TODO(erika): dict thing)
        """
        self.exps = exps


class IndexExp(LVal):
    def __init__(self, exp, index):
        """
        :param exp: Exp
        :param index: Exp
        """
        self.exp = exp
        self.index = index


class UnknownExp(Exp):
    pass


class UndefinedExp(Exp):
    pass


# TODO: Number, Boolean, String should maybe be a different 'val' type?
class NumberExp(Exp):
    def __init__(self, value):
        """
        :param value: number
        """
        self.value = value


class BooleanExp(Exp):
    def __init__(self, value):
        """
        :param value: boolean
        """
        self.value = value


class StringExp(Exp):
    def __init__(self, value):
        """
        :param value: string
        """
        self.value = value


class BinaryOpExp(Exp):
    def __init__(self, op, exp1, exp2):
        """
        :param op: BinaryOperator
        :param exp1: Exp
        :param exp2: Exp
        """
        self.op = op
        self.exp1 = exp1
        self.exp2 = exp2


class UnaryOpExp(Exp):
    def __init__(self, op, exp):
        """
        TODO(erika): not sure if should inherit from Exp
        :param op: UnaryOperator
        :param exp: Exp
        """
        self.op = op
        self.exp = exp


if __name__ == "__main__":
    s = StringExp("hello")
    binop = BinaryOpExp(BinaryOperator('+'), NumberExp(1), NumberExp(1))
    print(binop)