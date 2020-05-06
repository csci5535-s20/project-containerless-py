import ast
import astor

from ANF_transformer.transformer import _move_var_decls_to_top_of_scope


def test_move_var_decls_simple():
    node = ast.parse('a = 5\nb=2\na =b')

    #Input Code:
    #   a = 5
    #   b = 2
    #   a = b

    result_string, names_used = _move_var_decls_to_top_of_scope(node, {})
    astor_source_string_result = astor.to_source(result_string)

    test_string = 'a = None\nb = None\na = 5\nb = 2\na = b\n'
    #Expected Output Code:
    #   a = None
    #   b = None
    #   a = 5
    #   b = 2
    #   a = b
    assert(astor_source_string_result == test_string)



# def test_move_var_decls_multiple_scope_levels():
#     node = ast.parse('c=5 \ndef test():\n\tc = 5 \n\ta=5 \n\tif a == 5: \n\t\tb = 5 \nd=12 \nd += 12')
#     #Source:
#     #   c = 5
#     #   def test():
#     #       c = 5
#     #       a = 5
#     #       if a == 5:
#     #           b = 5
#     #   d=12
#     #   d += 12
#     result_string, names_used  = _move_var_decls_to_top_of_scope(node, {})
#     astor_source_string_result = astor.to_source(result_string)
#     test_string = 'c = None\nd = None\nc = 5\n\n\n' + \
#         'def test():\n    a = None\n    b = None\n    c = 5\n    a = 5\n' + \
#         '    if a == 5:\n        b = 5\n\n\nd = 12\nd += 12\n'
#
#     #Expected Output Source Code:
#     #   c = None
#     #   d = None
#     #   c = 5
#     #   def test():
#     #       a = None
#     #       b = None
#     #       c = 5
#     #       a = 5
#     #       if a == 5:
#     #           b = 5
#     #   d = 12
#     #   d += 12
#     assert(astor_source_string_result == test_string)
