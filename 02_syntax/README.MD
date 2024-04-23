#### 1.
Syntax analysis is the part where we use the previously defined tokens with lexer to check
that those tokens follow the rules written in the parser. There can be also recursive rules
etc. We can also use the same syntax parser to form the syntax tree after detecting the
syntax patterns correctly.

#### 2.
The syntax is formed by rules written in BNF that can depend on each other and can be 
recursive. We need first a lexer to collect the tokens to be syntax checked in the parser.

The syntaxes are formed using the rules and then storing the positional information of
the matched tokens. Then, those can be saved or printed or whatsoever.

#### 3.
##### a)
Variable definitions contain the matching variable name token, a left arrow and finally
the value for the variable and a dot.
##### b)
Function call consists of the name of a function, detected as a function name token,
and then a arrow to the right and finally the arguments after the arrow.
##### c)
Tuples have similar syntax to the variable definition. But instead it begins with the
list of values to be stored and then right arrow, and finally the name for the tuple.
Tuple names have angle brackets around them.

### 4.
##### a)
It is not by the syntax definition, since there are only variable definitions
allowed inside a function definition.
##### b)
It is allowed, since strings are also atoms and then factors and finally terms,
which can be combined with plus in the syntax def.
##### c)
It is possible. The atom rules allow to insert a const identifier so that allows to initialize
a variable with a constant.
##### d)
No, it is not possible. Constant value cannot be initialized by a variable value since
the syntax rules block this.
##### e)
It is not possible since the rules does not allow a double minus to be in
between atoms.
##### f)
It is done by adjusting the rules and the rule chain in a way that the mult/div rule is 
detected or used before the add/sub rule.

#### 5.
\-

#### 6.
Compared to the previous assignment, this was hell of a harder one. First of all, the
conversions between EBNF and BNF syntaxes added difficulty a lot. Also, some of the
definitions were requiring a lot of additional definitions to make them work correctly.

Almost nothing was easy in this phase. I did learn how to implement a syntax parser for
a lexer to detect if the occurrence of the tokens was correct.
