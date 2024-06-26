import lexer  # previous phase lexer code
from ply import yacc  # yacc parser from ply

# tokens are defined in lex-module, but needed here also in syntax rules
tokens = lexer.tokens


def p_program(p):
    '''program : return_value DOT
              | funcvar_recursive program'''
    # print("program")


def p_funcvar_recursive(p):
    '''funcvar_recursive : function_or_variable_definition
                         | function_or_variable_definition funcvar_recursive'''


def p_func_or_var(p):
    '''function_or_variable_definition : variable_definitions
                                        | function_definition '''
    # print("function or variable definition")


def p_func_body(p):
    '''function_body : function_or_variable_definition
                    | function_or_variable_definition function_body'''


def p_func_def(p):
    '''function_definition : DEFINE funcIDENT LSQUARE formals RSQUARE BEGIN function_body return_value DOT END DOT
                          | DEFINE funcIDENT LSQUARE RSQUARE BEGIN function_body return_value DOT END DOT
                          | DEFINE funcIDENT LSQUARE formals RSQUARE BEGIN return_value DOT END DOT
                          | DEFINE funcIDENT LSQUARE RSQUARE BEGIN return_value DOT END DOT'''
    print("func_definition({})".format(p[2]))


def p_formals(p):
    '''formals : varIDENT
                | varIDENT COMMA formals'''
    # print("formals")


def p_ret_val(p):
    '''return_value : EQ simple_expression
                   | NOTEQ pipe_expression'''
    # print("return_value")


def p_multi_var_def(p):
    '''variable_definitions : variable_definition
            | constant_definition
            | tuple_definition
            | tuple_pipe'''


def p_tuple_pipe(p):
    '''tuple_pipe : pipe_expression RARROW tupleIDENT DOT'''
    print("tuplevariable_definition({})".format(p[3]))


def p_var_def(p):
    '''variable_definition : varIDENT LARROW simple_expression DOT'''

    if p.slice[1].type == "constIDENT":
        print("constant_definition({})".format(p[1]))
    elif p.slice[1].type == "varIDENT":
        print("variable_definition({})".format(p[1]))
    elif p.slice[1].type == "tupleIDENT":
        print("tuple")


def p_const_def(p):
    '''constant_definition : constIDENT LARROW constant_expression DOT'''


def p_tuple_def(p):
    '''tuple_definition : tupleIDENT LARROW tuple_expression DOT'''


def p_const_expr(p):
    '''constant_expression : constIDENT
                        | NUMBER_LITERAL'''
    # print("constant_definition({})".format(p[1]))


def p_pipe_expr(p):
    '''pipe_expression : tuple_expression
                    | tuple_expression pipe_recursive'''
    print("pipe_expression")


def p_pipe_recursive(p):
    '''pipe_recursive : PIPE pipe_operation
                      | PIPE pipe_operation pipe_recursive'''


def p_pipe_oper(p):
    '''pipe_operation : funcIDENT
                 | MULT
                 | PLUS
                 | each_statement'''
    # print("pipe_operation")


def p_each(p):
    '''each_statement : EACH COLON funcIDENT'''
    # print("each_statement")


def p_tuple_expr(p):
    '''tuple_expression : tuple_atom
            | tuple_atom tuple_operation tuple_expression'''
    # print("tuple_expression")


def p_tuple_operation(p):
    '''tuple_operation : DOUBLEPLUS'''
    # print("tuple_operation")


def p_tuple_atom(p):
    '''tuple_atom : tupleIDENT
                | function_call
                | LSQUARE constant_expression DOUBLEMULT constant_expression RSQUARE
                | LSQUARE constant_expression DOUBLEDOT constant_expression RSQUARE
                | LSQUARE arguments RSQUARE'''
    # print("tuple_atom")


def p_func_call(p):
    '''function_call : funcIDENT LSQUARE RSQUARE
                    | funcIDENT LSQUARE arguments RSQUARE'''
    print("function_call({})".format(p[1]))


def p_args(p):
    '''arguments : simple_expression
                | simple_expression COMMA arguments'''
    # print("arguments")


def p_atom(p):
    '''atom : function_call
            | NUMBER_LITERAL
            | STRING_LITERAL
            | varIDENT
            | constIDENT
            | LPAREN simple_expression RPAREN
            | SELECT COLON constant_expression LSQUARE tuple_expression RSQUARE'''
    if len(p) == 2:
        print("atom({})".format(p[1]))
    else:
        print("atom")


def p_factor(p):
    '''factor : MINUS atom
             | atom'''
    print("factor")


def p_term(p):
    '''term : factor
            | term MULT factor
            | term DIV factor'''
    print("term")


def p_simple_expr(p):
    '''simple_expression : term
                        | term PLUS simple_expression
                        | term MINUS simple_expression'''
    print("simple_expression")


# def p_empty(p):
#     'empty :'
#     pass


# error token is generated by PLY if the automation enters error state
# (cannot continue reducing or shifting)
def p_error(p):
    try:
        print("{0}: Syntax Error (token:'{1}')".format(p.lineno, p.value))
    except AttributeError:
        print("End of file.")
    raise SystemExit


parser = yacc.yacc()

test = """
N <- 7.
PI <- 3.
ROUND <- 9.
= "this is an expression so it can be the last item in program".
"""

test2 = """
ab <- 7.
iI <- 999.
i9_abc <- 0.  a9 <- 9.
= "end".
"""

test3 = """
define Function[]
begin
  aa <- 0.
  = "return expr".
end.

= "last expression".
"""

test4 = """
N <- 7.
PI <- 3.
ROUND <- 9.

ab <- 7.
iI <- 999.

define Function[]
begin
  aa <- 0.
  = "return expr".
end.
i9_abc <- 0.  a9 <- 9.

= "last expression".
"""

test5 = """
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

test0 = """
define Funcname[] begin = 0. end.
define Func[] begin = 0. end.
= Func[1 , 2].
"""

test01 = """
N <- 7.
[1..N] | * -> <factorialten>.
"""

test02 = """
= Func[1,2].
"""

if __name__ == '__main__':
    '''
    result = parser.parse(test5)

    if result is None:
        print("SYNTAX OK")
    else:
        print(result)

    '''
    import argparse

    arg_parser = argparse.ArgumentParser()
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this')
    group.add_argument('-f', '--file', help='filename to process')
    ns = arg_parser.parse_args()

    if ns.who:
        # identify who wrote this
        print('123546 Sinipelto')
    elif ns.file is None:
        # user didn't provide input filename
        arg_parser.print_help()
    else:
        with open(ns.file) as INFILE:
            data = INFILE.read()
        result = parser.parse(data, lexer=lexer.lexer, debug=False)
        if result is None:
            print('syntax OK')

    # '''
