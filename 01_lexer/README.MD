1. 

Lexical analysis is the part of compilation where the source code file is read into the compiler program
and all the input is tried to be read and recognized as separate tokens using regular expressions.
If there are errors, the lexer usually stops and gives the programmer an error that there was an invalid token
on line x at pos y (if possible) or maybe it was an unexpected EOF. Once the tokens are collected, 
compiler moves to the syntax analysis phase.


2. 

All the known accepted tokens are in a list or tuple. There are maybe also explicitly defined some reserved
keywords that have a specific meaning in the programming language (e.g. for, while etc.). There are also
rules for ignored tokens, which are recognized but not stored anywhere, e.g. comments or whitespace.


3.

a) There is a dictionary containing the recognized words as keys and their corresponding tokens as values.
They are intially read as variables since they have similar syntax but there is a code that checks if the 
variable is a keyword.

b) Comments are completely ignored from the input. Comments start with { and end with }. There might be
nested comments also. Multiline comments should most of the time be recognized, too.

c) Whitespace is also ignored completely, meaning that whitespace does not affect the tokens read.
This means that one may write code with the whitespace of one's choice (eg. xx = 3 or xx=3 both will do).

d) They are recognzed as they are, in simple tokens that do not have any special regex.

e) Integer literals are every collection of digits written without whitespace.

f) String literals are started with " and ended with ". There can be multiple strings on same line but
multi-line strings are not recognized.

g) Functions name are strings that start with capital letter.

h) Tuples names are recognized as lowercase letters between < and >, inclusive.


4. 

a) Functions are tried to be processed before constants, so if there is any lowercase letters after one
capital letter, then it is read as a function. Otherwise it is a constant (only capitals).

b) Check 3a. Keywords are first read as variables but then a check is made if the variable name was a keyword.

c) Right arrow is tried to be read first so if there is no < or > found, it is passed onto minus regex.

d) String literals are inside quotes so anything inside quotes is string literal without quotes it could be 
a variable.

e) Comments are just excluded by reading any { and then } characters. Once found, they are ignored.

f) Tuple names can contain only lowercase alphabet inside < and > meaning that > would be missing from the
comparison and thus is not recognized as a tuple.


5.

I possibly implemented the nested comments handling, but it is not working in every possible input case.
Multiple comments are not implemented.


6.

This specific assignment was quite straightforward and had no bigger difficulties except getting the correct
regexes for some more complex inputs, eg. multiline comments, string literals when there may be anything inside
those. I did learn how to make a lexer that recognizes some simple tokens from a text file.