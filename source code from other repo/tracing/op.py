
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

    def __eq__(self, other):
        return isinstance(other, UnaryOperator) and (self.op == other.op)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return self.op

    def toJson(self):
        return self.op


class BinaryOperator:
    OPS = ['+', '-', '*', '**', '//', '/', '==', '!=', '>', '<', '>=', '<=', 'and', 'or']

    def __init__(self, op):
        if op in BinaryOperator.OPS:
            self.op = op
        else:
            raise ValueError("Unknown Binary Operator: {}".format(op))

    def __eq__(self, other):
        return isinstance(other, BinaryOperator) and (self.op == other.op)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return self.op

    def toJson(self):
        return self.op