import ast
import astor

from ANF_transformer import transformer

from .add_tracing import insert_tracing


def transform_program(code):
    normalized_code = transformer.normalize_to_ANF(code)
    ast_root = ast.parse(normalized_code)
    if isinstance(ast_root, ast.Module):
        traced_ast = insert_tracing(ast_root)
        code = astor.to_source(traced_ast)
        return _fix_lines_that_end_in_equal_sign(code)
    else:
        raise ValueError("Top Level Of Code Is Not A Module")

def _fix_lines_that_end_in_equal_sign(code):
    #some bug in astor splits lines on equal signs which is not valid.
    # this fixes by putting a \ at the end of the line.
    split_code = code.splitlines()
    for index, line in enumerate(split_code):
        if line.strip() and line.strip()[-1] == "=":
            reversed_line = line[::-1]
            line = "\ " + reversed_line
            line = line[::-1]
            split_code[index] = line

    return "\n".join(split_code)
