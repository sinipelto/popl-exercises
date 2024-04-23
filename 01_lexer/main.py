import argparse

import ply.lex as lex

# Reserved keywords as a map
reserved = {
    "define": "DEFINE",
    "begin": "BEGIN",
    "end": "END",
    "each": "EACH",
    "select": "SELECT",
}

# List of token names
tokens = [
    'LARROW',
    'RARROW',
    'LPAREN',
    'RPAREN',
    'LSQUARE',
    'RSQUARE',
    'COMMA',
    'DOT',
    'PIPE',
    'DOUBLEPLUS',
    'DOUBLEMULT',
    'DOUBLEDOT',
    'COLON',

    'EQ',
    'NOTEQ',
    'LT',
    'LTEQ',
    'GT',
    'GTEQ',
    'PLUS',
    'MINUS',
    'MULT',
    'DIV',
    'MOD',

             'STRING_LITERAL',
             'varIDENT',
             'constIDENT',
             'tupleIDENT',
             'funcIDENT',
             'NUMBER_LITERAL',

         ] + list(reserved.values())  # Add reserved keywords to recognized tokens


# Check that tokens is a set
if len(tokens) != len(set(tokens)):
    raise lex.LexError("Duplicate tokens found, aborting..", None)


# Regular expression rules for simple tokens

t_DOUBLEPLUS = r'\+\+'
t_DOUBLEMULT = r'\*\*'
t_DOUBLEDOT = r'\.\.'

t_LARROW = r'<-'
t_RARROW = r'->'

t_NOTEQ = r'!='
t_LTEQ = r'<='
t_GTEQ = r'>='

t_COLON = r':'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'

t_EQ = r'='


t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_MOD = r'%'

t_COMMA = r'\,'
t_DOT = r'\.'
t_PIPE = r'\|'


# More complex tokens
t_STRING_LITERAL = r'\"([^\\\"]|\\.)*\"'
t_tupleIDENT = r'<[a-z]+>'
t_funcIDENT = r'[A-Z][a-z0-9_]+'
t_constIDENT = r'[A-Z]+'


# A regular expression rule with some action code
def t_varIDENT(t):
    r'[a-z][a-zA-Z0-9_]+'
    t.type = reserved.get(t.value, 'varIDENT')  # Check for reserved words
    return t


# Catch literal numbers aka digits
def t_NUMBER_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Ignored tokens
t_ignore_COMMENT = r'{(.|\n)*}'

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    raise lex.LexError("Illegal character {} at line {}".format(t.value[0], t.lexer.lineno), None)


# Build the lexer
lexer = lex.lex()

# Some test cases below
test1 = '''message <- "Hello popl".
Print[message].
[ message, "again" ] | Print.
  '''

test2 = '''MEANING <- 42.
N <- 7.
variable <- 7 + 3.
<mytuple> <- [ 1 , 2, 1+2 ].
'''

test3 = '''define Squares[arg]
begin
  [arg * arg].
end.

[1..10] | each: Squares -> Print.
'''

popl = '''
str = "hello""test"""
testi {{  onkommentti HALOO
select 5{{ } inside each 3
{{{ConST {xy} kkk != 4
FooBar
FooFFBar
AFTERCOMMENT yk = 3
message <- "Hello popl".
Print[message].
[ message, "again" ] | Print.
T_e_st_ |||
'''

# Main function endpoint
if __name__ == '__main__':

    '''
    # Regular testing:

    # Give the lexer some input
    lexer.input(popl)

    # Read and parse tokens
    while True:
        # Run until out of tokens to parse
        tok = lexer.token()
        if not tok:
            break
        print(tok)
    '''

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this')
    group.add_argument('-f', '--file', help='filename to process')
    ns = parser.parse_args()

    if ns.who is True:
        # identify who wrote this
        print('123456 Sinipelto')
    elif ns.file is None:
        # user didn't provide input filename
        parser.print_help()
    else:
        with open(ns.file, 'r', encoding='utf-8') as INFILE:
            data = INFILE.read()

        # Give the file data as lexer input
        lexer.input(data)

        while True:
            token = lexer.token()
            if token is None:
                break
            print(token)
