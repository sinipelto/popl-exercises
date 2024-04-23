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
             'PLUS',
             'MINUS',
             'MULT',
             'DIV',
             'NUMBER_LITERAL',
             'STRING_LITERAL',
             'varIDENT',
             'constIDENT',
             'tupleIDENT',
             'funcIDENT',
         ] + list(reserved.values())  # Add reserved keywords to recognized tokens

# Check that tokens is a set
if len(tokens) != len(set(tokens)):
    raise lex.LexError("Duplicate tokens found, aborting..", None)

# More complex tokens
t_tupleIDENT = r'<[a-z]+>'
t_funcIDENT = r'[A-Z][a-z0-9_]+'
t_constIDENT = r'[A-Z]+'

# Regular expression rules for simple tokens
t_DOUBLEPLUS = r'\+\+'
t_DOUBLEMULT = r'\*\*'
t_DOUBLEDOT = r'\.\.'

t_LARROW = r'<-'
t_RARROW = r'->'

t_NOTEQ = r'!='

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

t_COMMA = r'\,'
t_DOT = r'\.'
t_PIPE = r'\|'


def t_STRING_LITERAL(t):
    r'\"([^\\\"]|\\.)*\"'
    t.value = t.value[1:len(t.value) - 1]
    return t


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
t_ignore_COMMENT = r'{.*}'

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character {0} at line {1}".format(t.value[0], t.lexer.lineno))
    exit()
    # raise lex.LexError("Illegal character {} at line {}".format(t.value[0], t.lexer.lineno), None)


# Build the lexer
lexer = lex.lex()

# Main function endpoint
if __name__ == '__main__':
    '''
    # Regular testing:

    # Give the lexer some input
    lexer.input(test5)

    # Read and parse tokens
    while True:
        # Run until out of tokens to parse
        tok = lexer.token()
        if not tok:
            break
        print(tok)
    '''
    import argparse, codecs

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
        with codecs.open(ns.file, 'r', encoding='utf-8') as INFILE:
            data = INFILE.read()

        # Give the file data as lexer input
        lexer.input(data)

        while True:
            token = lexer.token()
            if token is None:
                break
            print(token)
