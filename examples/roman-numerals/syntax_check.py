#!/usr/bin/env python3
# ----------------------------------------------------------------------
''' SuperSimple (and useless) unicodeLanguage. Numbers are roman numerals.
push 1 to stack, push 2 to stack, add them, print top of stack:
I⇑⍽II⇑⍽⊕⍽ψ⍽↵  
push 1 to stack, push 11 to stack, swap 1. and 2. item in stack, minus, print:
I⇑⍽XI⇑⍽↔⍽⊖⍽ψ⍽↵
push 1, 2, and 3 to stack, swap 2. and 3. elements in stack
I⇑⍽II⇑⍽III⇑⍽⟨II⍽III⍽↔⟩↵
push 2 and 1 to stack, create a copy of stack and perform addition+print,
return to original stack and perform subtraction+print
I⇑⍽II⇑⍽⟦⊕⍽ψ⟧⍽⊖⍽ψ↵
'''
# ----------------------------------------------------------------------
from ply import yacc
import tokenizer # previous phase example snippet code

# tokens are defined in lex-module, but needed here also in syntax rules
tokens = tokenizer.tokens

# any funcion starting with 'p_' is PLY yacc rule
# first definition is the target we want to reduce 
# in other words: after processing all input tokens, if this start-symbol
# is the only one left, we do not have any syntax errors
def p_program(p):
    '''program : statement
               | program statement'''
    print( 'program' )


# statement can be applied to number or standalone
def p_statement(p):
    '''statement : ROMAN unary_op
                 | single_op
                 | complex_stmt
                 | cmd_block'''
    if len(p) == 3:
        print( 'statement with ROMAN(', p[1], ')' )
    else:
        print( 'statement' )

def p_unary_op(p):
    '''unary_op : PUSH'''
    print( 'unary_op(', p[1], ')' )

def p_single_op(p):
    '''single_op : POP
                 | SWAP
                 | ADD
                 | SUB
                 | PRINT'''
    print( 'single_op(', p[1], ')' )

def p_complex_stmt(p):
    '''complex_stmt : CMDSTART ROMAN ROMAN complex_op CMDEND'''
    print( 'complex_op' )

def p_complex_op(p):
    '''complex_op : SWAP'''

def p_cmd_block(p):
    '''cmd_block : SEQSTART program SEQEND'''
    print( 'cmd_block' )

# error token is generated by PLY if the automation enters error state
# (cannot continue reducing or shifting)
def p_error(p):
    print( 'syntax error @', p )
    raise SystemExit

parser = yacc.yacc()

if __name__ == '__main__':
    import argparse, codecs
    arg_parser = argparse.ArgumentParser()
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this' )
    group.add_argument('-f', '--file', help='filename to process')
    ns = arg_parser.parse_args()
    if ns.who == True:
        # identify who wrote this
        print( '88888 Ahto Simakuutio' )
    elif ns.file is None:
        # user didn't provide input filename
        arg_parser.print_help()
    else:
        data = codecs.open( ns.file, encoding='utf-8' ).read()
        result = parser.parse(data, lexer=tokenizer.lexer, debug=False)
        if result is None:
            print( 'syntax OK' )

