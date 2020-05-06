import ast
import copy

import astor


def _convert_operator_to_string(operator):
    if isinstance(operator, ast.Add):
        return "+"
    elif isinstance(operator, ast.Sub) or isinstance(operator, ast.USub):
        return "-"
    elif isinstance(operator, ast.Mult):
        return "*"
    elif isinstance(operator, ast.Div):
        return "/"
    elif isinstance(operator, ast.Gt):
        return ">"
    elif isinstance(operator, ast.Lt):
        return "<"
    elif isinstance(operator, ast.GtE):
        return ">="
    elif isinstance(operator, ast.LtE):
        return "<="
    elif isinstance(operator, ast.Eq):
        return "=="

    raise ValueError("Operator Not Found")


def _trace_set(name, named):
    t_set_func = ast.Attribute(value=ast.Name('trace'), attr='trace_set')
    return ast.Expr(value=ast.Call(func=t_set_func, args=[ast.Str(name.id), named], keywords=[]))

def _trace_let(name, named):
    t_let_func = ast.Attribute(value=ast.Name('trace'), attr='trace_let')
    return ast.Expr(value=ast.Call(func=t_let_func, args=[ast.Str(name.id), named], keywords=[]))

def _trace_function_body(args):
    if len(args) > 1:
        targets = [ast.Tuple(elts=[ast.Name(id=arg+'000') for arg in args], ctx=ast.Store())]
    else:
        targets = [ast.Name(id=arg+'000') for arg in args]

    t_funcbody_func_name = ast.Attribute(value=ast.Name('trace'), attr='trace_function_body')
    t_funcbody_func = ast.Call(func=t_funcbody_func_name, args=[ast.Str('ret00')], keywords=[])

    args_assignemnt = ast.Assign(targets=targets, value=t_funcbody_func)

    return args_assignemnt

def _trace_function_call(result_name, args):
    t_funccall_func = ast.Attribute(value=ast.Name('trace'), attr='trace_function_call')
    return ast.Expr(value=ast.Call(func=t_funccall_func, args=[ast.Str(result_name.id), args], keywords=[]))

def _trace_args(args):
    #returns a list of a trace_let for each arg to the renamed arg form func body trace
    args = [_trace_let(ast.Name(id=arg, ctx=ast.Store()), ast.Name(id=arg +'000', ctx=ast.Load())) for arg in args]
    args.reverse()
    return args

def _trace_break(value):
    t_break_func = ast.Attribute(value=ast.Name('trace'), attr='trace_break')
    return ast.Expr(value=ast.Call(func=t_break_func, args=[ast.Str('ret00'), value], keywords=[]))

def _trace_if_true(condition):
    t_if_true_func = ast.Attribute(value=ast.Name('trace'), attr='trace_if_true')
    return ast.Expr(value=ast.Call(func=t_if_true_func, args=[condition], keywords=[]))

def _trace_if_false(condition):
    t_if_false_func = ast.Attribute(value=ast.Name('trace'), attr='trace_if_false')
    return ast.Expr(value=ast.Call(func=t_if_false_func, args=[condition], keywords=[]))


def _exp_binop(op, lhs, rhs):
    t_binop_func = ast.Attribute(value=ast.Name('exp'), attr='BinaryOpExp')
    return ast.Expr(value=ast.Call(func=t_binop_func, args=[ast.Str(s=op), lhs, rhs], keywords=[]))

def _exp_unary_op(op, rhs):
    t_unary_op_func = ast.Attribute(value=ast.Name('exp'), attr='UnaryOpExp')
    return ast.Expr(value=ast.Call(func=t_unary_op_func, args=[ast.Str(s=op), rhs], keywords=[]))

def _exp_identifier(identifier):
    name = identifier.id
    t_identifier_func = ast.Attribute(value=ast.Name('exp'), attr='IdExp')
    return ast.Expr(value=ast.Call(func=t_identifier_func, args=[ast.Str(s=name)], keywords=[]))

def _exp_num(number):
    value = number.n
    t_identifier_func = ast.Attribute(value=ast.Name('exp'), attr='NumberExp')
    return ast.Expr(value=ast.Call(func=t_identifier_func, args=[ast.Num(n=value)], keywords=[]))

def _exp_bool(bool):
    t_identifier_func = ast.Attribute(value=ast.Name('exp'), attr='BooleanExp')
    return ast.Expr(value=ast.Call(func=t_identifier_func, args=[bool], keywords=[]))

def _exp_none():
    t_unknown_func = ast.Attribute(value=ast.Name('exp'), attr='UndefinedExp')
    return ast.Expr(value=ast.Call(func=t_unknown_func, args=[], keywords=[]))

def _exp_new_trace():
    tracing = ast.Attribute(value=ast.Name('trace'), attr='new_trace')
    new_trace = ast.Expr(value=ast.Call(func=tracing, args=[], keywords=[]))
    return new_trace

def _exp_exit_block():
    tracing = ast.Attribute(value=ast.Name('trace'), attr='exit_block')
    exit_block = ast.Expr(value=ast.Call(func=tracing, args=[], keywords=[]))
    return exit_block

def _exp_index(name, index):
    t_index_func = ast.Attribute(value=ast.Name('exp'), attr='IndexExp')
    expr = ast.Expr(value=ast.Call(func=t_index_func,
           args=[_exp_identifier(name), _exp_num(index)], keywords=[]))
    return expr


def _transform_statement(vars_already_initilized, statement):

    transformed_statement = None
    if isinstance(statement, ast.Assign):
        if isinstance(statement.value, ast.Call):
            args = []
            function_name = ast.Str(s=statement.value.func.id)
            args.append(function_name)
            for arg in statement.value.args:
                vars_already_initilized, transformed_arg = _transform_statement(vars_already_initilized, arg)
                args.append(transformed_arg)
            args = ast.List(elts=args, ctx=ast.Load())
            transformed_statement = _trace_function_call(statement.targets[0], args)
        else:
            for target in statement.targets:
                #TODO:
                #Need soemthing to make sure multiple assignemnts
                #get traced to the right things. Ex. x, y = (1, 2)
                #if it's already defined - set it to new value.
                if target.id in vars_already_initilized:
                    vars_already_initilized, rhs = _transform_statement(vars_already_initilized, statement.value)
                    transformed_statement = _trace_set(target, rhs)
                else:
                #not defined yet, so trace it to a let.
                    vars_already_initilized, rhs = _transform_statement(vars_already_initilized, statement.value)
                    transformed_statement = _trace_let(target, rhs)
                    vars_already_initilized[target.id] = 1

    elif isinstance(statement, ast.FunctionDef):
        args = [arg.arg for arg in statement.args.args]

        #insert statements into function body
        statement.body = _transform_statements(statement.body, {})

        #create function body trace and insert in begining of function body.
        function_trace = _trace_function_body(args)
        statement.body.insert(0, function_trace)

        #create assignment for each arg and insert after function body trace call
        arg_assignments = _trace_args(args)
        for arg in arg_assignments:
            statement.body.insert(1, arg)

        transformed_statement = statement

    elif isinstance(statement, ast.Return):
        vars_already_initilized, return_expr = _transform_statement(vars_already_initilized, statement.value)
        transformed_statement = _trace_break(return_expr)

    elif isinstance(statement, ast.If):
        #only supports single conditions for now
        if isinstance(statement.test, ast.NameConstant):
            vars_already_initilized, conditional =  _transform_statement(vars_already_initilized, statement.test)
        else:
            vars_already_initilized, test_lhs = _transform_statement(vars_already_initilized, statement.test.left)
            op = _convert_operator_to_string(statement.test.ops[0])
            vars_already_initilized, test_rhs = _transform_statement(vars_already_initilized, statement.test.comparators[0])
            conditional = _exp_binop(op, test_lhs, test_rhs)

        name = 'test'
        while name in vars_already_initilized:
            name = name + '0'

        vars_already_initilized[name] = 1

        transformed_statement = [ast.Assign(targets=[ast.Name(id=name)], value=conditional)]

        statement.body = _transform_statements(statement.body, vars_already_initilized, False)
        statement.body.insert(0, _trace_if_true(ast.Name(id=name)))

        if statement.orelse:
            statement.orelse = _transform_statements(statement.orelse, vars_already_initilized, False)
            statement.orelse.insert(0, _trace_if_false(ast.Name(id=name)))

        transformed_statement.append(statement)

    elif isinstance(statement, ast.BinOp):

        vars_already_initilized, lhs = _transform_statement(vars_already_initilized, statement.left)
        op = _convert_operator_to_string(statement.op)
        vars_already_initilized, rhs = _transform_statement(vars_already_initilized, statement.right)

        transformed_statement = _exp_binop(op, lhs, rhs)

    elif isinstance(statement, ast.UnaryOp):

        op = _convert_operator_to_string(statement.op)
        vars_already_initilized, rhs = _transform_statement(vars_already_initilized, statement.operand)

        transformed_statement = _exp_unary_op(op, rhs)

    elif isinstance(statement, ast.Name):
        transformed_statement = _exp_identifier(statement)

    elif isinstance(statement, ast.Num):
        transformed_statement = _exp_num(statement)

    elif isinstance(statement, ast.NameConstant) and statement.value is None:
        transformed_statement = _exp_none()

    elif isinstance(statement, ast.NameConstant) and statement.value in [True, False]:
        transformed_statement = _exp_bool(statement)

    return vars_already_initilized, transformed_statement


def _transform_statements(body, vars_already_initilized, insert_exit_block=True):
    #iterate through body, inserting statements
    index = 0
    initial_body = copy.deepcopy(body)
    for statement in initial_body:
        #get tracing statement
        vars_already_initilized, new_statements = _transform_statement(vars_already_initilized, statement)
        #insert it above the old statement
        try:
            for new_statement in new_statements:
                body.insert(index, new_statement)
                index += 1
        except:
            body.insert(index, new_statements)
            index += 1

        if isinstance(statement, ast.FunctionDef) or isinstance(statement, ast.If):
            body.pop(index)
            index -= 1

        index += 1

    if insert_exit_block:
        #insert end block statement if needed. If return is last statement
        #don't put it after the return.
        index_to_insert = len(body)
        if isinstance(body[index_to_insert-1], ast.Return):
            index_to_insert -= 1

        body.insert(index_to_insert, _exp_exit_block())


    return body

def insert_tracing(ast_root):

    body = copy.deepcopy(_transform_statements(ast_root.body, {}))

    #information about user function
    user_func_name = body[0].name
    len_args_user_func = len(body[0].args.args)

    #get create new function serverless_function(trace, args)
    serverless_func = ast.FunctionDef(name='serverless_function', body=[body[0]],
          decorator_list=[],
          args=ast.arguments(
              args=[ast.arg('trace', annotation=None), ast.arg('args', annotation=None)],
              defaults=[], vararg=None, kwarg=None ))

    #index into args to get specific args
    args = [ast.Subscript(value= ast.Name(id='args'),
            slice=ast.Index(ast.Num(arg_num))) for arg_num in range(len_args_user_func)]

    #add tracing call for user function
    args_for_func_call = [_exp_identifier(ast.Name(id=user_func_name))]
    args_for_func_call.extend(
        [_exp_index(ast.Name(id="args"), ast.Num(i)) for i in range(len_args_user_func)])
    serverless_func.body.append(_trace_function_call(ast.Name('result'),
        ast.List(elts=args_for_func_call)))

    #add the call to the user func into the serverless function
    serverless_func.body.append(ast.Assign(targets=[ast.Name(id="result", ctx=ast.Store())],
        value=ast.Call(ast.Name(id=user_func_name), args=args, keywords=[])))

    #add return of result of user function to serverless function
    serverless_func.body.append(ast.Return(value=ast.Name(id='result')))

    #reset the body to be the resulting serverless function
    ast_root.body = [serverless_func]

     #insert import statement for expressions
    ast_root.body.insert(0,
        ast.Import(
         names=[ast.alias(name='tracing.exp',
         asname='exp')]))

    return ast_root
