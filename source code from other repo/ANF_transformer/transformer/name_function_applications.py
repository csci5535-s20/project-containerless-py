import ast

from .name_utils import _new_name

def _bring_function_calls_up(function_call, names_already_used):

    names_and_calls = {}
    for index, arg in enumerate(function_call.args):
        if isinstance(arg, ast.Call):
            name = _new_name('app', names_already_used)
            names_already_used[name] = 1
            lwr_names, names_already_used, arg = \
                _bring_function_calls_up(arg, names_already_used)

            names_and_calls[name] = arg
            names_and_calls.update(lwr_names)
            function_call.args[index] = ast.Name(id=name)

    return names_and_calls, names_already_used, function_call

def _name_unnamed_applications(node, names_already_used):
    if 'body' in node._fields:

        for index, statement in enumerate(node.body):
            try:
                if isinstance(statement.value, ast. Call):
                    #loop through args.
                    #If arg is function call replace with new name in args.
                    #save function call in list.
                    #loop through list putting let statement with every var
                    name_application = _new_name('app', names_already_used)
                    names_already_used[name_application] = 1
                    function_info = _bring_function_calls_up(statement.value, names_already_used)

                    new_calls = function_info[0]
                    names_already_used = function_info[1]
                    statement.value = function_info[2]
                    new_calls_keys = sorted(new_calls.keys())
                    new_calls_keys.reverse()
                    for new_call_name in new_calls_keys:
                        node.body.insert(index,
                            ast.Assign(targets=[ast.Name(id=new_call_name)],
                            value=new_calls[new_call_name]))
                        index += 1

                    if isinstance(statement, ast.Expr):
                        #Have to re initilize the call of for some reason, astor puts it on a new line otherwise.
                        node.body[index] = ast.Assign(targets=[ast.Name(id=name_application, ctx=ast.Store)],
                            value=ast.Call(statement.value.func, statement.value.args, statement.value.keywords))
            except AttributeError:
                pass

        for child in ast.iter_child_nodes(node):
            child, names_already_used = _name_unnamed_applications(child, names_already_used)

    return node, names_already_used
