import ast
import astor

from ANF_transformer.transformer import _make_for_loops_while

def test_make_for_loops_while_loops():
    src_string = \
"""
y = []
x = [1, 2, 3]
for index in range(len(x)):
    y[index] = x[index]
"""
    source_ast = ast.parse(src_string)
    test_ast, test_names_in_use = _make_for_loops_while(source_ast, {})

    result_string = \
"""y = []
loop_index0 = 0
x = [1, 2, 3]
while loop_index0 < len(range(len(x))):
    index = range(len(x))[loop_index0]
    y[index] = x[index]
    loop_index0 += 1
"""
    #names in use tracks the current variable names in use.
    #converting for to while loops should add any new names used to
    #this hash table.
    result_names_in_use = {'loop_index0': 1}
    print(astor.to_source(test_ast))
    print(result_string)

    assert(test_names_in_use == result_names_in_use)
    assert(astor.to_source(test_ast) == result_string)
