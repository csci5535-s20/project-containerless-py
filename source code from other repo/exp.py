from abc import ABCMeta


class UnaryOperator:
    """
    TODO: We may want to remove 'not' at first, as it has a lot of different functions within Python
    i.e. in comparisons, None is not, 0 is not, '' is not, etc. Or at least we could limit the functionality
    we support to booleans at this point.
    """
    OPS = ['not', '-']

    def __init__(self, op):
        if op in BinaryOperator.OPS:
            self.op = op
        else:
            raise ValueError("Unknown Unary Operator: {}".format(op))


class BinaryOperator:
    OPS = ['+', '-', '*', '**', '//', '/', '==', '!=', '>', '<', '>=', '<=', 'and', 'or']

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
    TODO(erika): we may not need this, but I want to leave it here for now.
    """
    pass


class BlockExp(Exp):
    """
    | Block
    """
    def __init__(self, body):
        """
        :param body: a list of expressions, Exp[]
        """
        self.body = body


class LetExp(Exp):
    """
    | Name = Exp
    """
    def __init__(self, name, exp):
        self.name = name
        self.exp = exp


class SetExp(Exp):
    """
    | Exp.Name = Exp
    """
    def __init__(self, leftval, exp):
        self.leftval = leftval
        self.exp = exp


class IfExp(Exp):
    """
    | if Expr: Block else: Block
    """
    def __init__(self, condition, true_part, false_part):
        self.condition = condition
        self.true_part = true_part
        self.false_part = false_part


class WhileExp(Exp):
    """
    | while Exp: Block
    """
    def __init__(self, condition, body):
        """
        :param condition:
        :param body: A list of expressions
        """
        self.condition = condition
        self.body = body


class CallbackExp(Exp):
    def __init__(self, event, event_arg, callback_args, clos, body):
        """
        TODO(erika): Waiting to see how things play out before deciding to keep/remove this.
        There's no directly analogous case in our expression syntax.


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
    | Exp( <Exp> *) -- function call
    """
    def __init__(self, event, event_args):
        self.event = event
        self.event_args = event_args


class IdExp(LVal):
    """
    Class representing an identifier

    | Name
    """
    def __init__(self, name):
        self.name = name


class GetExp(Exp):
    """
    Note from JS: "A GetExp reads a value out of an object"

    | Expr.Name -- attribute access
    """
    def __init__(self, exp, field):
        self.exp = exp
        self.field = field


class ArrayExp(Exp):
    """
    | [ <Exp> *] - Literal List
    """

    def __init__(self, exps):
        """
        :param properties: tenv (TODO(erika): dict thing)
        """
        self.exps = exps


class GetIndexExp(LVal):
    """
    | Exp[Exp]                    -- Slice access
    TODO(erika): This should (maybe?) apply to both dictionaries and lists??
    """
    def __init__(self, exp, index):
        """
        :param exp: Exp
        :param index: Exp
        """
        self.exp = exp
        self.index = index


class SetIndexExp(Exp):
    """
    | Exp[Exp] = Exp    -- slice assignment
    TODO(erika): This should (maybe?) apply to both dictionaries and lists??
    """
    def __init__(self, exp, index, value):
        self.exp = exp
        self.index = index
        self.value = value


class ReturnExp(Exp):
    """
    | return Exp
    """
    def __init__(self, exp):
        self.exp = exp


class FunctionDefinitionExp(Exp):
    """
    | def Name( <Name> *) : Block
    """
    def __init__(self, name, args, block):
        self.name = name
        self.args = args
        self.block = block


class UnknownExp(Exp):
    pass


class UndefinedExp(Exp):
    pass


# TODO: Number, Boolean, String should maybe be a different 'val' type instead of exp?
class NumberExp(Exp):
    """
    | Int   - Literal integer
    """
    def __init__(self, value):
        """
        :param value: number
        """
        self.value = value


class BooleanExp(Exp):
    """
    | Bool - Boolean
    """
    def __init__(self, value):
        """
        :param value: boolean
        """
        self.value = value


class StringExp(Exp):
    """
    | String
    """
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
        :param op: UnaryOperator
        :param exp: Exp
        """
        self.op = op
        self.exp = exp


'''

TODO(erika): no direct analogous expression in our expression syntax, but I'll leave the code here for now.

class FromExp(LVal):
    """
    Note from JS: "A FromExp reads a value out of a closure, thus needs to be derefenced
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


class ClosExp(Exp):
    def __init__(self, tenv):
        """
        :param tenv: tenv (TODO(erika): dict thing)
        """
        self.tenv = tenv


class ObjExp(Exp):
    def __init__(self, properties):
        """
        :param properties: tenv (TODO(erika): dict thing)
        """
        self.properties = properties

'''


if __name__ == "__main__":
    s = StringExp("hello")
    binop = BinaryOpExp(BinaryOperator('+'), NumberExp(1), NumberExp(1))
    print(binop)