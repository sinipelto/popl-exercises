import lexer  # previous phase lexer code
import tree_print  # module to print the syntax tree
from ply import yacc  # yacc parser from ply

# tokens are defined in lex-module, but needed here also in syntax rules
tokens = lexer.tokens


class ASTnode:
    def __init__(self, typestr):
        self.nodetype = typestr


def p_program(p):
    '''program : statement'''
    p[0] = ASTnode("program")
    # p[0].child_ = ASTnode("stmt")
    p[0].children_ = [p[1]]
    # print("program")


def p_program_rec(p):
    '''program : statement program'''
    p[0] = ASTnode("program")
    # p[0].child_ = ASTnode("program_rec")
    p[0].children_ = [p[1], p[2]]
    # print("program_recursive")


def p_stmt_ret(p):
    '''statement : return_value DOT'''
    p[0] = ASTnode("stmt_ret")
    # p[0].child_ = ASTnode("return_value_dot")
    p[0].children_ = [p[1], p[2]]


def p_stmt_func(p):
    '''statement : function_body'''
    p[0] = ASTnode("stmt_func")
    # p[0].child_ = ASTnode("function_body")
    p[0].children_ = [p[1]]


def p_func_body(p):
    '''function_body : function_or_variable_definition'''
    p[0] = ASTnode("func_body")
    # p[0].child_ = ASTnode("func_var")
    p[0].children_ = [p[1]]
    # print("func body")


def p_func_body_rec(p):
    '''function_body : function_or_variable_definition function_body'''
    p[0] = ASTnode("func_body_rec")
    # p[0].child_ = ASTnode("func_var")
    p[0].children_ = [p[1], p[2]]
    # print("func_body_rec")


def p_funcvar_var(p):
    '''function_or_variable_definition : variable_definitions'''
    p[0] = ASTnode("funcvar_var")
    # p[0].child_ = ASTnode("var_defs")
    p[0].children_ = [p[1]]
    # print("variable_definition")


def p_funcvar_func(p):
    '''function_or_variable_definition : function_definitions '''
    p[0] = ASTnode("funcvar_func")
    # p[0].child_ = ASTnode("func_def")
    p[0].children_ = [p[1]]
    # print("function_definition")


def p_func_def(p):
    '''function_definitions : formals_body
                          | noformals_body
                          | formals_nobody
                          | noformals_nobody'''
    p[0] = ASTnode("func_def_list")
    # p[0].child_ = ASTnode("func_def_sel")
    p[0].children_ = [p[1]]
    # print("function_definitions")


def p_form_body(p):
    '''formals_body : DEFINE funcIDENT LSQUARE formals RSQUARE BEGIN function_body return_value DOT END DOT'''
    p[0] = ASTnode("formals_body")
    # p[0].child_ = ASTnode("form_body")
    p[0].children_ = [p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11]]
    # print("formals_body")


def p_form_nobody(p):
    '''formals_nobody : DEFINE funcIDENT LSQUARE formals RSQUARE BEGIN return_value DOT END DOT'''
    p[0] = ASTnode("formals_nobody")
    # p[0].child_ = ASTnode("form_nobody")
    p[0].children_ = [p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10]]
    # print("formals_nobody")


def p_noparam_body(p):
    '''noformals_body : DEFINE funcIDENT LSQUARE RSQUARE BEGIN function_body return_value DOT END DOT'''
    p[0] = ASTnode("noformals_body")
    # p[0].child_ = ASTnode("noform_body")
    p[0].children_ = [p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10]]
    # print("noformals_body")


def p_noparam_nobody(p):
    '''noformals_nobody : DEFINE funcIDENT LSQUARE RSQUARE BEGIN return_value DOT END DOT'''
    p[0] = ASTnode("noformals_nobody")
    # p[0].child_ = ASTnode("noform_nobody")
    p[0].children_ = [p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9]]
    # print("noformals_nobody")


def p_formals_var(p):
    '''formals : varIDENT'''
    p[0] = ASTnode("formals_var")
    # p[0].child_ = ASTnode("var")
    p[0].children_ = [p[1]]
    # print("formals_var")


def p_formals_comma(p):
    '''formals : comma_formals'''
    p[0] = ASTnode("formals_comma")
    # p[0].child_ = ASTnode("comma_formals")
    p[0].children_ = [p[1]]
    # print("formals_comma")


def p_com_form(p):
    '''comma_formals : varIDENT COMMA formals'''
    p[0] = ASTnode("comma_expr")
    # p[0].child_ = ASTnode("comma_formals_def")
    p[0].children_ = [p[1], p[2], p[3]]
    # print("comma_formals")


def p_eq_retval(p):
    '''return_value : EQ simple_expression'''
    p[0] = ASTnode("ret_val_eq")
    # p[0].child_ = ASTnode("simple_expr")
    p[0].children_ = [p[1], p[2]]
    # print("eq_retval")


def p_noteq_retval(p):
    '''return_value : NOTEQ pipe_expression'''
    p[0] = ASTnode("ret_val_noteq")
    # p[0].child_ = ASTnode("pipe_expr")
    p[0].children_ = [p[1], p[2]]
    # print("noteq_retval")


def p_var_defs(p):
    '''variable_definitions : variable_definition
            | constant_definition
            | tuple_definition
            | tuple_pipe'''
    p[0] = ASTnode("var_def_list")
    # p[0].child_ = ASTnode("vartype_def")
    p[0].children_ = [p[1]]
    # print("var_defs")


def p_tuple_pipe(p):
    '''tuple_pipe : pipe_expression RARROW tupleIDENT DOT'''
    p[0] = ASTnode("tuple_pipe")
    # p[0].child_ = ASTnode("tuple_pipe_expr")
    p[0].children_ = [p[1], p[2], p[3], p[4]]
    # print("tuplevariable_definition({})".format(p[3]))


def p_var_def(p):
    '''variable_definition : varIDENT LARROW simple_expression DOT'''
    p[0] = ASTnode("vardef_var")
    # p[0].child_ = ASTnode("var_def")
    p[0].children_ = [p[1], p[2], p[3], p[4]]
    # print("variable_definition({})".format(p[1]))


def p_const_def(p):
    '''constant_definition : constIDENT LARROW constant_expression DOT'''
    p[0] = ASTnode("vardef_const")
    # p[0].child_ = ASTnode("const_def")
    p[0].children_ = [p[1], p[2], p[3], p[4]]
    # print("constant_definition({})".format(p[1]))


def p_tuple_def(p):
    '''tuple_definition : tupleIDENT LARROW tuple_expression DOT'''
    p[0] = ASTnode("vardef_tuple")
    # p[0].child_ = ASTnode("tuple_def")
    p[0].children_ = [p[1], p[2], p[3], p[4]]
    # print("tuple_def")


def p_const_expr_const(p):
    '''constant_expression : constIDENT'''
    p[0] = ASTnode("const_expr_const")
    # p[0].child_ = ASTnode("const")
    p[0].children_ = [p[1]]
    # print("constant_expression_const({})".format(p[1]))


def p_const_expr_num(p):
    '''constant_expression : NUMBER_LITERAL'''
    p[0] = ASTnode("const_expr_num")
    # p[0].child_ = ASTnode("num_literal")
    p[0].children_ = [p[1]]
    # print("constant_expression_num({})".format(p[1]))


def p_pipe_tuple_expr(p):
    '''pipe_expression : tuple_expression'''
    p[0] = ASTnode("pipe_tuple_expr")
    # p[0].child_ = ASTnode("tuple_expr")
    p[0].children_ = [p[1]]
    # print("pipe_expr")


def p_pipe_tuple_expr_rec(p):
    '''pipe_expression : tuple_expression pipe_recursive'''
    p[0] = ASTnode("pipe_tuple_rec")
    # p[0].child_ = ASTnode("pipe_rec")
    p[0].children_ = [p[1], p[1]]
    # print("pipe_expr_rec")


def p_pipe_op(p):
    '''pipe_recursive : PIPE pipe_operation'''
    p[0] = ASTnode("pipe_op")
    # p[0].child_ = ASTnode("pipe_op_def")
    p[0].children_ = [p[1], p[2]]


def p_pipe_op_rec(p):
    '''pipe_recursive : PIPE pipe_operation pipe_recursive'''
    p[0] = ASTnode("pipe_op_rec")
    # p[0].child_ = ASTnode("pipe_rec_def")
    p[0].children_ = [p[1], p[2], p[3]]


def p_pipe_func(p):
    '''pipe_operation : funcIDENT'''
    p[0] = ASTnode("pipe_func")
    # p[0].child_ = ASTnode("func")
    p[0].children_ = [p[1]]
    # print("pipe_operation_func")


def p_pipe_mult(p):
    '''pipe_operation : MULT'''
    p[0] = ASTnode("pipe_mult")
    # p[0].child_ = ASTnode("mult")
    p[0].children_ = [p[1]]
    # print("pipe_operation_mult")


def p_pipe_plus(p):
    '''pipe_operation : PLUS'''
    p[0] = ASTnode("pipe_plus")
    # p[0].child_ = ASTnode("plus")
    p[0].children_ = [p[1]]
    # print("pipe_operation_plus")


def p_pipe_each(p):
    '''pipe_operation : each_statement'''
    p[0] = ASTnode("pipe_each")
    # p[0].child_ = ASTnode("each_stmt")
    p[0].children_ = [p[1]]
    # print("pipe_operation_each")


def p_each(p):
    '''each_statement : EACH COLON funcIDENT'''
    p[0] = ASTnode("each_stmt")
    # p[0].child_ = ASTnode("each_stmt_def")
    p[0].children_ = [p[1], p[2], p[3]]
    # print("each_statement")


def p_tuple_expr_atom(p):
    '''tuple_expression : tuple_atom'''
    p[0] = ASTnode("tuple_expr_atom")
    # p[0].child_ = ASTnode("tuple_atom")
    p[0].children_ = [p[1]]
    # print("tuple_expression")


def p_tuple_expr_op(p):
    '''tuple_expression : tuple_atom tuple_operation tuple_expression'''
    p[0] = ASTnode("tuple_expr_op")
    # p[0].child_ = ASTnode("tuple_atom_op")
    p[0].children_ = [p[1], p[2], p[3]]
    # print("tuple_expression")


def p_tuple_operation(p):
    '''tuple_operation : DOUBLEPLUS'''
    p[0] = ASTnode("tuple_op")
    # p[0].child_ = ASTnode("doubleplus")
    p[0].children_ = [p[1]]
    # print("tuple_operation")


def p_tuple_atom_tuple(p):
    '''tuple_atom : tupleIDENT'''
    p[0] = ASTnode("tuple_atom_tuple")
    # p[0].child_ = ASTnode("tuple")
    p[0].children_ = [p[1]]
    # print("tuple_atom_tuple")


def p_tuple_atom_func(p):
    '''tuple_atom : function_call'''
    p[0] = ASTnode("tuple_atom_func")
    # p[0].child_ = ASTnode("func_call")
    p[0].children_ = [p[1]]
    # print("tuple_atom")


def p_tuple_atom_mult(p):
    '''tuple_atom : LSQUARE constant_expression DOUBLEMULT constant_expression RSQUARE'''
    p[0] = ASTnode("tuple_atom_mult")
    # p[0].child_ = ASTnode("doublemult_expr")
    p[0].children_ = [p[1], p[2], p[3], p[4], p[5]]
    # print("tuple_atom_mult")


def p_tuple_atom_dot(p):
    '''tuple_atom : LSQUARE constant_expression DOUBLEDOT constant_expression RSQUARE'''
    p[0] = ASTnode("tuple_atom_dot")
    # p[0].child_ = ASTnode("doubledot_expr")
    p[0].children_ = [p[1], p[2], p[3], p[4], p[5]]
    # print("tuple_atom_dot")


def p_tuple_atom_arg(p):
    '''tuple_atom : LSQUARE arguments RSQUARE'''
    p[0] = ASTnode("tuple_atom_arg")
    # p[0].child_ = ASTnode("arg_expr")
    p[0].children_ = [p[1], p[2], p[3]]
    # print("tuple_atom_arg")


def p_func_call_noarg(p):
    '''function_call : funcIDENT LSQUARE RSQUARE'''
    p[0] = ASTnode("func_call_noarg")
    # p[0].child_ = ASTnode("call_noarg")
    p[0].children_ = [p[1], p[2], p[3]]
    # print("function_call_noarg({})".format(p[1]))


def p_func_call_arg(p):
    '''function_call : funcIDENT LSQUARE arguments RSQUARE'''
    p[0] = ASTnode("func_call_arg")
    # p[0].child_ = ASTnode("call_arg")
    p[0].children_ = [p[1], p[2], p[3], p[4]]
    # print("function_call_arg({})".format(p[1]))


def p_args(p):
    '''arguments : simple_expression'''
    p[0] = ASTnode("arg_simple")
    # p[0].child_ = ASTnode("simple_expr")
    p[0].children_ = [p[1]]
    # print("arguments")


def p_args_rec(p):
    '''arguments : simple_expression COMMA arguments'''
    p[0] = ASTnode("arg_rec")
    # p[0].child_ = ASTnode("arg_simple_rec")
    p[0].children_ = [p[1], p[3], p[2]]
    # print("arguments_recursive")


def p_atom_call(p):
    '''atom : function_call'''
    p[0] = ASTnode("atom_call")
    # p[0].child_ = ASTnode("func_call")
    p[0].children_ = [p[1]]
    # print("func_call")


def p_atom_num(p):
    '''atom : NUMBER_LITERAL'''
    p[0] = ASTnode("atom_num")
    # p[0].child_ = ASTnode("num_literal")
    p[0].children_ = [p[1]]
    # print("atom_number")


def p_atom_str(p):
    '''atom : STRING_LITERAL'''
    p[0] = ASTnode("atom_str")
    # p[0].child_ = ASTnode("str_literal")
    p[0].children_ = [p[1]]
    # print("atom_string")


def p_atom_var(p):
    '''atom : varIDENT'''
    p[0] = ASTnode("atom_var")
    # p[0].child_ = ASTnode("var")
    p[0].children_ = [p[1]]
    # print("atom_var")


def p_atom_const(p):
    '''atom : constIDENT'''
    p[0] = ASTnode("atom_const")
    # p[0].child_ = ASTnode("const")
    p[0].children_ = [p[1]]
    # print("atom_const")


def p_atom_simple(p):
    '''atom : LPAREN simple_expression RPAREN'''
    p[0] = ASTnode("atom_simple")
    # p[0].child_ = ASTnode("simple_paren")
    p[0].children_ = [p[1], p[2], p[3]]
    # print("atom_simple_expr")


def p_atom_const_tuple(p):
    '''atom : SELECT COLON constant_expression LSQUARE tuple_expression RSQUARE'''
    p[0] = ASTnode("atom_const_tuple")
    # p[0].child_ = ASTnode("const_tuple")
    p[0].children_ = [p[1], p[2], p[3], p[4], p[5], p[6]]
    # print("atom_constupl")


def p_factor_minus(p):
    '''factor : MINUS atom'''
    p[0] = ASTnode("factor_minus")
    # p[0].child_ = ASTnode("minus_atom")
    p[0].children_ = [p[1]]
    # print("factor_minus")


def p_factor_atom(p):
    '''factor : atom'''
    p[0] = ASTnode("factor")
    # p[0].child_ = ASTnode("atom")
    p[0].children_ = [p[1]]
    # print("factor_atom")


def p_term_fact(p):
    '''term : factor'''
    p[0] = ASTnode("term")
    # p[0].child_ = ASTnode("factor")
    p[0].children_ = [p[1]]
    # print("term")


def p_term_mult(p):
    '''term : term MULT factor'''
    p[0] = ASTnode("term_mult")
    # p[0].child_ = ASTnode("term_mult")
    p[0].children_ = [p[1], p[2], p[3]]
    # print("term")


def p_term_div(p):
    '''term : term DIV factor'''
    p[0] = ASTnode("term_div")
    # p[0].child_ = ASTnode("term_div")
    p[0].children_ = [p[1], p[2], p[3]]
    # print("term")


def p_simple_expr(p):
    '''simple_expression : term'''
    p[0] = ASTnode("simple_expr_term")
    # p[0].child_ = ASTnode("term")
    p[0].children_ = [p[1]]
    # print("simple_expression")


def p_simple_expr_plus(p):
    '''simple_expression : term PLUS simple_expression'''
    p[0] = ASTnode("simple_expr_plus")
    # p[0].child_ = ASTnode("term_plus")
    p[0].children_ = [p[1], p[2], p[3]]
    # print("simple_expr_plus")


def p_simple_expr_minus(p):
    '''simple_expression : term MINUS simple_expression'''
    p[0] = ASTnode("simple_expr_minus")
    # p[0].child_ = ASTnode("term_minus")
    p[0].children_ = [p[1], p[2], p[3]]
    # print("simple_expr_minus")


# error token is generated by PLY if the automation enters error state
# (cannot continue reducing or shifting)
def p_error(p):
    try:
        print("{0}: Syntax Error (token:'{1}')".format(p.lineno, p.value))
    except AttributeError as e:
        print(e)
        print("Unexpected end of file.")
        return
    raise SystemExit


test1 = """
N <- 7.
PI <- 3.
ROUND <- 9.
= "this is an expression so it can be the last item in program".
"""

bigger = """
{ This tries to be a "bigger" and "concrete" example using many features of the Tupl language. }

{ Calculate the factorial of N. }
N <- 10.
[1..N] | * -> <factorialten>.
["I know that 10! is "] ++ <factorialten> | Print -> <dummyvar>.

{ A function that prints a value and it doubled, returns the doubled value. }
define Print_and_double[aa]
begin
  [aa, " doubled is", 2*aa] | Print -> <tuple>.
  = select:3[<tuple>]. { return the 3. element of tuple. }
end.

{ Keyword each calls a function for every element in a tuple. }
[1,5,2,8,4,5] | each:Print_and_double -> <doubles>.
<doubles> | + -> <sumofdoubles>.
sum <- select:1[<sumofdoubles>].
!= Print["Sum of doubles is ", sum].
"""

parser = yacc.yacc()

if __name__ == '__main__':
    '''
    outformat = "ascii"
    result = parser.parse(bigger, lexer=lexer.lexer, debug=False)
    print("\n*****SYNTAX TREE*****\n")
    tree_print.treeprint(result, outformat)
    print("\n*****END OF SYNTAX TREE*****\n")

    '''
    import argparse

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-t', '--treetype', help='type of output tree (unicode/ascii/dot)')
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this')
    group.add_argument('-f', '--file', help='filename to process')
    ns = arg_parser.parse_args()

    outformat = "unicode"
    if ns.treetype:
        outformat = ns.treetype

    if ns.who:
        # identify who wrote this
        print('123456 Sinipelto')
    elif ns.file is None:
        # user didn't provide input filename
        arg_parser.print_help()
    else:
        with open(ns.file) as FILE:
            data = FILE.read()
        result = parser.parse(data, lexer=lexer.lexer, debug=False)
        tree_print.treeprint(result, outformat)

    # '''
