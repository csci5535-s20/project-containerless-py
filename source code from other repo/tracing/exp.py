from abc import ABCMeta, abstractmethod
import json


class ExpressionMergeException(Exception):
    pass


class Exp(metaclass=ABCMeta):
    """
    This abstract class takes the place of the abstract datatype for expressions, Exp
    """

    @abstractmethod
    def merge(self, other):
        """
        This method takes the place of merge_exp, which is a helper version in the JS implementation
        It will throw an ExpressionMergeException if the expressions cannot be merged, and nothing otherwise.

        Despite the fact that it is called merge, it is more a 'check for equality' than an actual merge operation
        :param other: Expression to compare self to
        :return: None
        :raises: ExpressionMergeException
        """
        pass

    @classmethod
    def merge_exp_array(cls, arr1, arr2):
        """
        Utility method to merge two arrays of expressions
        :param arr1: Array of expressions
        :param arr2: A second array of expressions
        :return: None
        :raises: ExpressionMergeException
        """
        if len(arr1) != len(arr2):
            raise ExpressionMergeException("Cannot merge expression arrays of different lengths")
        for i in range(len(arr1)):
            arr1[i].merge(arr2[i])

    @abstractmethod
    def toJson(self):
        """
        Expressions must be JSON serializable, since the outputted trace is assumed to be JSON.
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

    def merge(self, other):
        if not isinstance(other, BlockExp):
            raise ExpressionMergeException("Expected expression of type BlockExp, got {}".format(type(other)))
        Exp.merge_exp_array(self.body, other.body)

    def __repr__(self):
        return "BlockExp({})".format(self.body)

    def toJson(self):
        return{'kind': 'block', 'body': self.body}


class LetExp(Exp):
    """
    | Name = Exp
    """
    def __init__(self, name, named):
        self.name = name
        self.named = named

    def merge(self, other):
        if not isinstance(other, LetExp):
            raise ExpressionMergeException("Expected expression of type LetExp, got {}".format(type(other)))
        if self.name != other.name:
            raise ExpressionMergeException("Let name mismatch: {} != {}".format(self.name, other.name))
        self.named.merge(other.named)

    def __repr__(self):
        return "LetExp({}, {})".format(self.name, self.named)

    def toJson(self):
        return {'kind': 'let', 'name': self.name, 'named': self.named}


class SetExp(Exp):
    """
    | Exp.Name = Exp
    """
    def __init__(self, name, named):
        self.name = name
        self.named = named

    def merge(self, other):
        if not isinstance(other, SetExp):
            raise ExpressionMergeException("Expected expression of type SetExp, got {}".format(type(other)))
        if self.name != other.name:
            raise ExpressionMergeException("Set name mismatch: {} != {}".format(self.name, other.name))
        self.named.merge(other.named)

    def __repr__(self):
        return "SetExp({}, {})".format(self.name, self.named)

    def toJson(self):
        return {'kind': 'set', 'name': self.name, 'named': self.named.toJson()}


class IfExp(Exp):
    """
    | if Expr: Block else: Block
    """
    def __init__(self, condition, true_part, false_part):
        self.condition = condition
        self.true_part = true_part
        self.false_part = false_part

    def merge(self, other):
        if not isinstance(other, IfExp):
            raise ExpressionMergeException("Expected expression of type IfExp, got {}".format(type(other)))
        self.condition.merge(other.condition)
        Exp.merge_exp_array(self.true_part, other.true_part)
        Exp.merge_exp_array(self.false_part, other.false_part)

    def __repr__(self):
        return "IfExp({}, {}, {})".format(self.condition, self.true_part, self.false_part)

    def toJson(self):
        return {'kind': 'if', 'condition': self.condition, 'true_part': self.true_part,
                'false_part': self.false_part}


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

    def merge(self, other):
        if not isinstance(other, WhileExp):
            raise ExpressionMergeException("Expected expression of type WhileExp, got {}".format(type(other)))
        self.condition.merge(other.condition)
        Exp.merge_exp_array(self.body, other.body)

    def __repr__(self):
        return "WhileExp({}, {})".format(self.condition, self.body)

    def toJson(self):
        return {'kind': 'while', 'condition': self.condition.toJson(), 'body': self.body.toJson}


class CallbackExp(Exp):
    def __init__(self, event, event_arg, callback_args, clos, body):
        """
        There's no directly analogous case in our expression syntax.
        Used for initial function invocation
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

    def merge(self, other):
        raise ExpressionMergeException("Cannot merge callback expressions. "
                                       "tracer.trace_callback removes the need for it.")

    def __repr__(self):
        return "CallbackExp({}, {}, {}, {}, {})".format(self.event, self.event_arg, self.callback_args, self.clos,
                                                        self.body)

    def toJson(self):
        return {'kind': 'callback', 'event': self.event.toJson(),
                'event_arg': self.event_arg.toJson(),
                'callback_args': self.callback_args,
                'clos': self.clos, 'body': self.body}


class PrimAppExp(Exp):
    """
    | Exp( <Exp> *) -- function call
    """
    def __init__(self, event, event_args):
        self.event = event
        self.event_args = event_args

    def merge(self, other):
        raise ExpressionMergeException("Cannot merge primapp expressions. "
                                       "tracer.trace_primapp removes the need for it.")

    def __repr__(self):
        return "PrimAppExp({}, {})".format(self.event, self.event_args)

    def toJson(self):
        return {'kind': 'primApp', 'event': self.event.toJson(), 'event_args': self.event_args.toJson()}


class LabelExp(Exp):
    """
    No corresponding Python - used during function tracing
    """
    def __init__(self, name, body):
        self.name = name
        self.body = body

    def merge(self, other):
        if not isinstance(other, LabelExp):
            raise ExpressionMergeException("Expected expression of type LabelExp, got {}".format(type(other)))
        if self.name != other.name:
            raise ExpressionMergeException("Name mismatch: {} != {}".format(self.name, other.name))
        Exp.merge_exp_array(self.body, other.body)

    def __repr__(self):
        return "LabelExp({}, {})".format(self.name, self.body)

    def toJson(self):
        return {'kind': 'label', 'name': self.name, 'body': self.body}


class BreakExp(Exp):
    """
    No corresponding Python - used during function tracing
    """

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def merge(self, other):
        if not isinstance(other, BreakExp):
            raise ExpressionMergeException("Expected expression of type BreakExp, got {}".format(type(other)))
        if self.name != other.name:
            raise ExpressionMergeException("Name mismatch: {} != {}".format(self.name, other.name))

    def __repr__(self):
        return "BreakExp({}, {})".format(self.name, self.value)

    def toJson(self):
        return {'kind': 'break', 'name': self.name, 'value': self.value}


class IdExp(Exp):
    """
    Class representing an identifier

    | Name
    """
    def __init__(self, name):
        self.name = name

    def merge(self, other):
        if not isinstance(other, IdExp):
            raise ExpressionMergeException("Expected expression of type IdExp, got {}".format(type(other)))
        if self.name != other.name:
            raise ExpressionMergeException("Name mismatch: {} != {}".format(self.name, other.name))

    def __repr__(self):
        return "IdExp({})".format(self.name)

    def toJson(self):
        return {'kind': 'identifier', 'name': self.name}


class FromExp(Exp):
    """
     A FromExp reads a value out of a closure, thus needs to be deferenced.
    """
    def __init__(self, exp, field):
        self.exp = exp
        self.field = field

    def merge(self, other):
        if not isinstance(other, FromExp):
            raise ExpressionMergeException("Expected expression of type FromExp, got {}".format(type(other)))
        if self.field != other.field:
            raise ExpressionMergeException("Field mismatch: {} != {}".format(self.field, other.field))
        self.exp.merge(other.exp)

    def __repr__(self):
        return "FromExp({}, {})".format(self.exp, self.field)

    def toJson(self):
        return {'kind': 'from', 'exp': self.exp.toJson(), 'field': self.field.toJson()}


class GetExp(Exp):
    """
    Note from JS: "A GetExp reads a value out of an object"

    | Expr.Name -- attribute access
    """
    def __init__(self, exp, field):
        self.exp = exp
        self.field = field

    def merge(self, other):
        if not isinstance(other, GetExp):
            raise ExpressionMergeException("Expected expression of type GetExp, got {}".format(type(other)))
        if self.field != other.field:
            raise ExpressionMergeException("Field mismatch: {} != {}".format(self.field, other.field))
        self.exp.merge(other.exp)

    def __repr__(self):
        return "GetExp({}.{})".format(self.exp, self.field)

    def toJson(self):
        return {'kind': 'get', 'exp': self.exp.toJson(), 'field': self.field.toJson()}


class ArrayExp(Exp):
    """
    | [ <Exp> *] - Literal List
    """

    def __init__(self, exps):
        """
        :param exps: tenv)
        """
        self.exps = exps

    def merge(self, other):
        if not isinstance(other, ArrayExp):
            raise ExpressionMergeException("Expected expression of type ArrayExp, got {}".format(type(other)))
        Exp.merge_exp_array(self.exps, other.exps) # TODO: will probably be key/value store and not array

    def __repr__(self):
        return "ArrayExp({})".format(self.exps)

    def toJson(self):
        return {'kind': 'array', 'exps': self.exps.toJson()}


class IndexExp(Exp):
    def __init__(self, exp, index):
        self.exp = exp
        self.index = index

    def merge(self, other):
        if not isinstance(other, IndexExp):
            raise ExpressionMergeException("Expected expression of type ArrayExp, got {}".format(type(other)))
        self.exp.merge(other.exp)
        self.index.merge(other.index)

    def __repr__(self):
        return "IndexExp({}, {})".format(self.exp, self.index)

    def toJson(self):
        return {'kind': 'index', 'exp': self.exp.toJson(), 'index': self.index.toJson()}


class ObjExp(Exp):
    """
        Represents an object
    """
    def __init__(self, properties):
        self.properties = properties  # Should be dict of key/values

    def merge(self, other):
        if not isinstance(other, ObjExp):
            raise ExpressionMergeException("Expected expression of type ObjExp, got {}".format(type(other)))
        for k in self.properties.keys():
            if k in other.properties.keys:
                self.properties[k].merge(other.properties[k])
            else:
                raise ExpressionMergeException("Property mismatch: {}".format(k))

    def __repr__(self):
        return "ObjExp({})".format(self.properties)

    def toJson(self):
        return {'kind': 'object', 'properties': self.properties}


class ClosExp(Exp):
    def __init__(self, tenv):
        self.tenv = tenv

    def merge(self, other):
        if not isinstance(other, ClosExp):
            raise ExpressionMergeException("Expected expression of type ClosExp, got {}".format(type(other)))
        for k in self.tenv.keys():
            if k in other.tenv.keys:
                self.tenv[k].merge(other.tenv[k])
            else:
                raise ExpressionMergeException("Property mismatch: {}".format(k))

    def __repr__(self):
        return "ClosExp({})".format(self.tenv)

    def toJson(self):
        return {'kind': 'clos', 'tenv': self.tenv}


class MethodCallExp(Exp):
    """
    | def Name( <Name> *) : Block
    """
    def __init__(self, exp, method, args):
        self.exp = exp
        self.method = method
        self.args = args

    def merge(self, other):
        if not isinstance(other, MethodCallExp):
            raise ExpressionMergeException(
                "Expected expression of type MethodCallExp, got {}".format(type(other)))
        if self.method != other.method:
            raise ExpressionMergeException("MethodCallExp methods don't match: {} != {}".format(
                self.method, other.method))
        self.exp.merge(other.exp)
        Exp.merge_exp_array(self.args, other.args)

    def __repr__(self):
        return "MethodCallExp({}, {}, {})".format(self.exp, self.method, self.args)

    def toJson(self):
        return {'kind': 'methodCall', 'e': self.exp.toJson(), 'method': self.method,
                'methodCallArgs': self.args}


class UnknownExp(Exp):
    def __init__(self):
        pass

    def merge(self, other):
        if not isinstance(other, UnknownExp):
            raise ExpressionMergeException("Expected expression of type UnknownExp, got {}".format(type(other)))

    def __repr__(self):
        return "UnknownExp()"

    def toJson(self):
        return {'kind': 'unknown'}


class UndefinedExp(Exp):
    def __init__(self):
        pass

    def merge(self, other):
        if not isinstance(other, UndefinedExp):
            raise ExpressionMergeException("Expected expression of type UndefinedExp, got {}".format(type(other)))

    def __repr__(self):
        return "UndefinedExp()"

    def toJson(self):
        return {'kind': 'undefined'}


class NumberExp(Exp):
    """
    | Int   - Literal integer
    """
    def __init__(self, value):
        """
        :param value: number
        """
        self.value = value

    def merge(self, other):
        if not isinstance(other, NumberExp):
            raise ExpressionMergeException("Expected expression of type NumberExp, got {}".format(type(other)))
        if self.value != other.value:
            raise ExpressionMergeException("Value mismatch: {} != {}".format(self.value, other.value))

    def __repr__(self):
        return "NumberExp({})".format(self.value)

    def toJson(self):
        return {'kind': 'number', 'value': self.value}


class BooleanExp(Exp):
    """
    | Bool - Boolean
    """
    def __init__(self, value):
        """
        :param value: boolean
        """
        self.value = value

    def merge(self, other):
        if not isinstance(other, BooleanExp):
            raise ExpressionMergeException("Expected expression of type BooleanExp, got {}".format(type(other)))
        if self.value != other.value:
            raise ExpressionMergeException("Value mismatch: {} != {}".format(self.value, other.value))

    def __repr__(self):
        return "BooleanExp({})".format(self.value)

    def toJson(self):
        return {'kind': 'boolean', 'value': self.value}


class StringExp(Exp):
    """
    | String
    """
    def __init__(self, value):
        """
        :param value: string
        """
        self.value = value

    def merge(self, other):
        if not isinstance(other, StringExp):
            raise ExpressionMergeException("Expected expression of type StringExp, got {}".format(type(other)))
        if self.value != other.value:
            raise ExpressionMergeException("Value mismatch: {} != {}".format(self.value, other.value))

    def __repr__(self):
        return "StringExp(\"{}\")".format(self.value)

    def toJson(self):
        return {'kind': 'string', 'value': self.value}


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

    def merge(self, other):
        if not isinstance(other, BinaryOpExp):
            raise ExpressionMergeException("Expected expression of type BinaryOpExp, got {}".format(type(other)))
        if self.op != other.op:
            raise ExpressionMergeException("Operation mismatch: {} != {}".format(self.op, other.op))
        self.exp1.merge(other.exp1)
        self.exp2.merge(other.exp2)

    def __repr__(self):
        return "BinOpExp({}, {}, {})".format(self.exp1, self.op, self.exp2)

    def toJson(self):
        return {'kind': 'binop', 'op': self.op, 'e1': self.exp1.toJson(), 'e2': self.exp2.toJson()}


class UnaryOpExp(Exp):
    def __init__(self, op, exp):
        """
        :param op: UnaryOperator
        :param exp: Exp
        """
        self.op = op
        self.exp = exp

    def merge(self, other):
        if not isinstance(other, UnaryOpExp):
            raise ExpressionMergeException("Expected expression of type UnaryOpExp, got {}".format(type(other)))
        if self.op != other.op:
            raise ExpressionMergeException("Operation mismatch: {} != {}".format(self.op, other.op))
        self.exp.merge(other.exp)

    def __repr__(self):
        return "UnaryOpExp({}, {})".format(self.op, self.exp)

    def toJson(self):
        return {'kind': 'op1', 'op': self.op, 'e': self.exp.toJson()}


if __name__ == "__main__":
    s = StringExp("hello")
    print(json.dumps(s.toJson(), default=lambda o : o.toJson()))

    l = LetExp(IdExp('foo'), NumberExp(2))
    print(json.dumps(l.toJson(), default=lambda o : o.toJson()))
