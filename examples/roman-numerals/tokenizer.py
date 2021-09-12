#!/usr/bin/env python3
# ----------------------------------------------------------------------
''' SuperSimple (and useless) unicodeLanguage. Numbers are roman numerals.

push 1 to stack, push 2 to stack, add them, print top of stack:
I⇑⍽II⇑⍽⊕⍽ψ⍽↵  

push 1 to stack, push 11 to stack, swap 1. and 2. item in stack, minus, print:
I⇑⍽XI⇑⍽↔⍽⊖⍽ψ⍽↵

push 1, 2, and 3 to stack, swap 2. and 3. elements in stack
I⇑⍽II⇑⍽III⇑⍽⟨II⍽III⍽↔⟩

push 2 and 1 to stack, create a copy of stack and perform addition+print,
return to original stack and perform subtraction+print
I⇑⍽II⇑⍽⟦⊕⍽ψ⟧⍽⊖⍽ψ↵
'''


# ----------------------------------------------------------------------
# support routines for roman numerals conversion
# source: https://www.safaribooksonline.com/library/view/python-cookbook/0596001673/ch03s24.html

def int_to_roman(input):
    if not 0 < input < 4000:
        raise ValueError( "to_roman: Argument must be between 1 and 3999" )
    ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
    nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
    result = []
    for i in range(len(ints)):
        count = int(input / ints[i])
        result.append(nums[i] * count)
        input -= ints[i] * count
    return ''.join(result)

def roman_to_int(input : str) -> int:
    """ Convert a Roman numeral to an integer. """

    nums = {'M':1000, 'D':500, 'C':100, 'L':50, 'X':10, 'V':5, 'I':1}
    sum = 0
    for i in range(len(input)):
        value = nums[input[i]]
        # If the next place holds a larger number, this value is negative
        if i+1 < len(input) and nums[input[i+1]] > value:
            sum -= value
        else: sum += value
    if int_to_roman(sum) == input:
        return sum 
    else:
        raise ValueError( "'{}' not a valid roman number".format(input) )


# ----------------------------------------------------------------------
import sys, ply.lex

tokens = ( 'PUSH', 'POP', 'SWAP', 'ADD', 'SUB', 'PRINT', 'ROMAN', 'CMDSTART', 'CMDEND', 'SEQSTART', 'SEQEND', 'EOL' )

t_PUSH = r'⇑'
t_POP  = r'⇓' 
t_SWAP = r'↔'
t_ADD  = r'⊕'
t_SUB  = r'⊖'
t_PRINT= r'ψ'
t_CMDSTART=r'⟨'
t_CMDEND=r'⟩'
t_SEQSTART=r'⟦'
t_SEQEND=r'⟧'

def t_ROMAN(t):
    r'[MDCLXVI]+'  # valid chars for a roman number, can be invalid format
    t.value = roman_to_int( t.value )
    return t

# count line number we are processing
def t_EOL(t):
    r'↵'
    t.lexer.lineno += 1

t_ignore = '⍽\n'

def t_error(t):
    raise Exception("Illegal character '{}' at line {}".format( 
        t.value[0], t.lexer.lineno ) )

# define lexer in module level so it can be used after 
# importing this module:
lexer = ply.lex.lex()

# if this module/file is the first one started (the main module)
# then run:
if __name__ == '__main__':
    import argparse, codecs
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this' )
    group.add_argument('-f', '--file', help='filename to process')

    ns = parser.parse_args()
    if ns.who == True:
        # identify who wrote this
        print( '88888 Ahto Simakuutio' )
    elif ns.file is None:
        # user didn't provide input filename
        parser.print_help()
    else:
        # using codecs to make sure we process unicode
        with codecs.open( ns.file, 'r', encoding='utf-8' ) as INFILE:
            # blindly read all to memory (what if that is a 42Gb file?)
            data = INFILE.read() 

        lexer.input( data )

        while True:
            token = lexer.token()
            if token is None:
                break
            print( token )


