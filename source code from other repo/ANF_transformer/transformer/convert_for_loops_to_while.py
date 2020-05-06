import ast

from .name_utils import _new_name


def _make_for_loops_while(parent_node, names_in_use):
    """Converts for loops into while loops.
    Creates an index variable and a call to the len() function as a test for the while loop.
    All for loop iterators must be indexable. DOES NOT SUPPOT NONINDEXABLE ITERATORS.
    Parameters:
        parent_node: ast node
    Returns:
        parent node with updates"""

    #get every index of for loop objects in the body of parent node. Could be done cleaner with a numpy .where,
    #but we'd have to import numpy pretty much just for that.
    try:
        indices_of_for_loops = list(filter(lambda index: isinstance(parent_node.body[index], ast.For),
                                            range(len(parent_node.body))))
    except:
        #node has no body. No for loops in it.
        return parent_node, names_in_use

    for for_loop_index in indices_of_for_loops:
        for_loop = parent_node.body[for_loop_index]

        #make loop incrementor variable
        name_incrementor_variable = _new_name('loop_index', names_in_use)
        names_in_use[name_incrementor_variable] = 1

        #make a call to built in len() function with the iterator provided in the for loop
        len_builtin_function = ast.Name(id='len', ctx=ast.Load)
        len_function_call = ast.Call(func=len_builtin_function, args=[for_loop.iter], keywords=[])

        #test for while loop
        compare_op = ast.Compare(ast.Name(name_incrementor_variable, ctx=ast.Load),
             ops=[ast.Lt()], comparators=[len_function_call])

        #assign current value of loop to for loop target
        assign_to_for_loop_target = ast.Assign([for_loop.target],
            ast.Subscript(for_loop.iter, ast.Index(ast.Name(id=name_incrementor_variable, ctx=ast.Load))))

        #increment index variable
        add_1_to_index_variable = ast.AugAssign(ast.Name(id=name_incrementor_variable), ast.Add(), ast.Num(1))

        #construct while loop
        while_loop_body = [assign_to_for_loop_target] + \
            for_loop.body + [add_1_to_index_variable]
        while_loop = ast.While(test=compare_op, body= while_loop_body, orelse=[])

        #replace for with while loop
        parent_node.body[for_loop_index] = while_loop

        #insert loop incrementor variabel before while loop and set to 0
        parent_node.body.insert(for_loop_index - 1,
            ast.Assign([ast.Name(id=name_incrementor_variable, ctx=ast.Store)], ast.Num(0)))

    return parent_node, names_in_use
