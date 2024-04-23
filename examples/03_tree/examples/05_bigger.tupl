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
