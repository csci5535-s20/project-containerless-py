import ast

from ANF_transformer.transformer import _new_name
from ANF_transformer.transformer import _get_all_used_variable_names


def test_get_new_name_does_not_dupclicate_names():
    name = 'x'
    names_already_used = ['x', 'x0', 'x1']
    assert(_new_name(name, names_already_used) == 'x2')

def test_get_all_used_variable_names_gets_all_names_in_use():
    node = ast.parse(
"""
import ast
def func():
    x = [1, 2, 3]
    len_x = len(x)
    for y in x:
        pass
""")
    names_used = {'ast': None, 'func': None, 'x': None, 'len_x': None, 'y': None, 'len': None}
    assert(_get_all_used_variable_names(node) == names_used)
