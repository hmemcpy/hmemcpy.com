+++
title = "Functional Programming in Haskell (Stepik course notes) - module 1"
date = 2020-01-18T02:01:20Z
+++
There's a fantastic free online course (MOOC) for the Russian-speaking developer community on [Stepik](https://stepik.org/) for learning Haskell - a two-part course titled [Functional Programming in Haskell](https://stepik.org/course/75) by Denis Moskvin, (then) associate professor at the St. Petersburg Academic University. I recently re-watched the course (having completed it previously) and decided to take notes and summarize the course content in English for your enjoyment.

I would like to thank Denis Moskvin for providing this amazing resource for free, and urge you, if you speak Russian and want to learn Haskell, to work through the course material and exercises!

Below is the summary of the first module, **Introduction**, out of 5.

<!-- more -->

1. **Introduction** (this page)
2. [Programming fundamentals](/2020/01/functional-programming-in-haskell-stepik-course-notes-module-2/)
3. Lists
4. Data types
5. Monads

---

## Introduction

*Note:* The original Stepik course was recorded using GHC version 7.6.3. At the time of writing this series, the latest available GHC version is 8.8.2, which may include some differences. Mainly, since version 8 of the GHC, using the keyword `let` inside GHCi is no longer required when defining functions.

### Installing and configuring GHC

Download and install the [Haskell Platform](https://www.haskell.org/platform/) for your operating system.

The Haskell Platform contains the Glasgow Haskell Compiler (GHC), the interpreter environment (GHCi, also known as "REPL"), as well as other tools.

Haskell source code is written in text files having the `.hs` extension. Most text editors support the Haskell syntax in the form of syntax highlighting and code completion. Haskell uses significant indentation for scoping. Use spaces to indent your code to prevent compilation errors.

#### Using the interpreter (GHCi)

To start the interpreter, type `ghci` in your command shell:

```
 $ ghci
GHCi, version 8.6.5: http://www.haskell.org/ghc/  :? for help
Prelude> _
```
The standard module `Prelude` gets loaded automatically, it contains many standard types and useful functions.

We can start typing expressions into the interpreter:

```
Prelude> 33 + 3 * 3
42
```

The interpreter will compute the expression and will display the result in the next line.

We can type other kinds of expressions, such as the function `pi`:

```
Prelude> pi
3.141592653589793
Prelude> "ABC" ++ "DE"
"ABCDE"
```

The default prompt can be changed using the command `:set prompt`, followed by the new prompt name:

```
Prelude> :set prompt "GHCi> "
GHCi> _
```

Note that changing the default prompt hides the name of the currently loaded module, and as such, not recommended.

#### Working with modules

Create a new text file with the following definition:

```haskell
module Test where

sayHello = putStrLn "Hello from module Test!"
```

Save the file with the name `test.hs` (in the same directory where GHCi was started), then load the file using the `:load` command:

```
Prelude> :load Test
[1 of 1] Compiling Test             ( Test.hs, interpreted )
Ok, one module loaded.
*Test> sayHello
Hello from module Test!
*Test> _
```

Another handy command is `:reload`, allowing you to reload the module after changing it in the text editor. Changing **Hello from module Test!** to **Hello World from module Test!**, saving the file, and typing `:reload` in GHCi:

```
*Test> :reload
[1 of 1] Compiling Test             ( Test.hs, interpreted )
Ok, one module loaded.
*Test> sayHello
Hello World from module Test!
*Test> _
```

Most commands can be shortened to the first letter (unless ambiguous) - instead of `:load` and `:reload` we can type `:l` and `:r`, respectively.

### Functions

In imperative languages, programs are sequences of instructions that are executed, and their result is stored in memory locations of the runtime, called variables. Subsequent instructions can refer to previous results stored in those variables. In most imperative languages, variables can be modified during the execution of the program.

In functional languages, programs are expressions, and executing the program means *reducing* those expressions until it's no longer possible to reduce it further. Reduced expressions are the result of the program execution.

Here's an example of a mathematical expression, and its reduction steps:

```
(5 + 4 * 3) ^ 2
 ~> (5 + 12) ^ 2
 ~> 17 ^ 2
 ~> 289
```

The first line contains the body of the expression, and each subsequent line is the reduction step. The resulting expression which cannot be further reduced is the final result 289. In future modules we'll use the squiggly-arrow ~> to describe reduction steps of an expression.

#### Function application

Let's talk about applying functions and the role of parentheses.

We'll start by writing two identifiers, `foo` and `bar`:

```
> foo bar
```

Those identifiers are not defined anywhere, but syntactically they mean "apply the function `foo` to the argument `bar`". In other languages, we usually place the argument in parentheses, e.g. `foo(bar)` in the C language. In Haskell, calling a function does not require placing its arguments in parentheses, but rather they are used to group sequences of functions together.

In the following expression:

```
> acos (cos pi)
3.141592653589793
```
we first calculate the result of applying `cos` to `pi` followed by applying `acos` to the result.

If a function takes multiple parameters, they are applied in order, separated by a space:

```
> max 5 42
42
```

Here we're applying the function `max`, which takes two arguments, to the values `5` and `42`. This function returns the larger of the two arguments, resulting in 42.

Another, equivalent form of writing the previous expression is as follows:

```
> (max 5) 52
42
```

This equivalence is called left-associativity. It is said that function application associates to the left, causing the two-argument function `max` to be applied first to the value 5, resulting in a one-argument function, which is further applied to 42.

Applying functions to just some of its arguments is called *partial application*. In this form, `(max 5)` is a partially-applied function that expects an additional argument to produce a result. Suppose the expression:

```
> 3 + sin 42
2.0834784520843663
```

In this expression, `sin` is a function that expects one argument. We can replace it with our partially applied `(max 5)`:

```
> 3 + (max 5) 42
45
```

Here, the result of `(max 5)` applied to 42 will be 42, which will be added with 3 to result in the value 45.

Partial application is a very powerful tool. In Haskell we can formalize it as follows: a function of *n* arguments can be viewed as a function of *one* argument, returning a function of *n - 1* arguments.

#### Declaring functions

To define a function we need to give it a name, followed by its parameters, followed by the `=` sign, after which we specify the function body. Let's define a function that sums the squares of its two arguments:

```
sumSquares x y = x ^ 2 + y ^ 2

     ^     ^ ^   ^^^^^^^^^^^^^
     |     | |   |
     |     | |   +-- function body
     |     | +------ second argument
     |     +-------- first argument 
     +-------------- function name
```

After defining this function, we can now call it:

```
> sumSquares 1 2
5
```

Haskell requires all functions and formal parameter names to start with a lowercase letter. Names starting with an uppercase letter are used to define data types. Haskell function names can contain numbers (as long as they're not the first letter), as well as underscores, and a single quote (`'`) is often used. The name `rock'n'roll` is a valid Haskell identifier.

#### Pure functions

What sets Haskell apart from many other programming languages if the fact that Haskell functions are *pure* - the meaning of a Haskell function is completely specified by its input arguments. No other inputs can influence the result of a pure function. It is said that a pure function has no *side-effects*. As a result, a function that does not take any arguments is a *constant* - it will always yield the same result.

The following function:

```
> fortyTwo = 39 + 3
> fortyTwo
42
```

Will always produce the value 42, regardless of when and where it is executed. It is not possible in Haskell to define a function of no arguments that returns different results on different calls. To create functions that produce random values we will need to use a special *container* called `IO`, which will be introduced in later modules.

#### Conditions

Many programming languages contain a conditional operator `if`, that is used to branch program execution, depending on some condition. In imperative languages, the `if` condition may or may not be followed by an `else` branch. Haskell also contains a conditional `if` operator that is syntactically similar to the imperative one.

Let's define a function `f`:

```
> f x = if x > 0 then 1 else (-1)
> f 5
1
> f (-5)
-1
```

This function takes a numeric value `x` and returns 1 if `x` is greater than 0, otherwise -1. When used as arguments, negative numbers in Haskell must be enclosed in parentheses, e.g. (-5) means the argument -5.

Functional languages like Haskell require both branches `then` and `else` to be defined. Both branches must contain expressions of the same type, otherwise, it will be a compilation error. The other major difference between functional and imperative languages is the fact that conditionals are expressions too. It means that conditional expressions could be used in building other, larger expressions:

```
> g x = (if x > 0 then 1 else (-1)) + 3
> g 5
4
> g (-7)
2
```

Here in function `g`, we add 3 to the result of the conditional expression.

#### Partial application

Let's suppose we want to define a function `max5` which takes a single argument. It will return this argument if it's greater than 5, otherwise 5. We can use the existing `max` function:

```
> max5 x = max 5 x
> max5 4
5
> max5 42
42
```

In Haskell, we can write a shorter version of this function, by dropping the argument `x` on both sides of the equals sign. Let's call it `max5'`:

```
> max5' = max 5
> max5' 4
5
> max5' 42
42
```

It behaves exactly as `max5`, but here the partial application is more obvious: the function `max` is partially applied to the value 5, resulting in a function of a single argument. This style of defining a function without specifying all of the parameters is quite pervasive in Haskell, and it's called the *point-free* style.

Let's look at another example, a function `discount` that calculates a discount given some percentage if the sum is greater than some limit:

```
> discount limit pct sum = if sum >= limit then sum * (100 - pct) / 100 else sum
```

The order of parameters in this definition is a little weird. In Haskell, oftentimes functions are designed to prioritize making partial application convenient. In the case of our `discount` function, we suppose that the arguments `limit` and `pct` would rarely change, while the `sum` argument may be different each time. We can introduce another function, `standardDiscount`, which offers a standard discount of 5% for sums over 1000:

```
> discount limit pct sum = if sum >= limit then sum * (100 - pct) / 100 else sum
> standardDiscount = discount 1000 5
```

This is a partially-applied function, the parameter `sum` is not specified on either side (although it could have been). We can now call the `standardDiscount` function with just one parameter:

```
> standardDiscount 2000
1900.0
> standardDiscount 900
900
```

### Operators

Operators exist in Haskell just like functions but are called in a slightly different style. Suppose the expression `max 6 7`. It is written in a so-called *prefix* style, where the function name `max` is prefixing the arguments. In contrast, operators are usually written in an *infix* style, e.g. `6 + 7` - the operator `+` is infixed between its two arguments.

```
> max 6 7
7
> 6 + 7
13
```

However, in Haskell, this distinction can be removed by writing functions in an infix ("operator") style, and operators in a prefix ("functional") style. Functions surrounded by backticks (`` ` ``) and written between the arguments can be used as operators:

```
> 6 `max` 7
7
```

To use operators in a functional style, they have to be placed in parentheses:

```
> (+) 6 7
13
```

Nearly all operators in Haskell are binary, meaning they accept two arguments. In the example above we turned the binary operator `+` to a binary function `(+)` applied to two arguments. The only exception is the unary `-` operator which negates numeric values. To avoid collisions between binary and unary `-` we enclose negative numbers in argument positions in parentheses:

```
> - 7
-7
> (-) 5 3
2
> max (-5) 5
5
```

#### Operator precedence and associativity

Suppose the following expression:

```
> 3 + 5 * 8
43
```

From mathematics, we know that multiplication precedes addition. Haskell also knows about this, because the addition and multiplication operators have a certain *precedence*. The multiplication operator has a higher precedence than addition, and Haskell uses this information when evaluating the expression.

A precedence level is a number from 0 to 9, bigger means higher. Function application in Haskell is considered having a precedence level 10 - highest possible, which is why the expression `sin 5 + 4` is first evaluated by calculating `sin 5` and then adding 4 to the result. All operators have lower precedence than function application.

Associativity is taken into account when operators lack associativity rules. The expression `3 - 9 - 5` could be viewed in two ways:

```
> (3 - 9) - 5
-11
```

also known as *left-associative*, or

```
> 3 - (9 - 5)
-1
```
known as *right-associative*.

From mathematics, subtraction is a left-associative operation, and Haskell will give us the correct result without using any parentheses:

```
> 3 - 9 - 5
-11
```

To define operator associativity, Haskell uses the keywords `infixl` and `infixr` for left and right associativity, respectively, or `infix` for operators without associativity rules. The keyword is followed by the precedence level and the operator name.

Here are some operators defined in the standard library:

```haskell
infixr 8 ^, `logBase`
infixl 7 *, `div`, `mod`
infixl 6 +, -
infix 4 ==, /=, >, >=, <, <=
```

Using functions in operator (infix) style, such as `logBase` will have defined associativity and precedence levels. In this case, `logBase` in operator mode is right-associative, having precedence level 8.

Any operator lacking a fixity declaration is assumed to be `infixl 9`.

#### Operator definition

Haskell does not have built-in operators. All operators used until now (`+`, `*`, etc.) are defined in the standard library. Haskell allows users to define custom operators, using a combination of any of the following symbols:

```
! # $ % & * + . / < = > ? @ \ ^ | - ~
```

The symbol `:` can also be used, but it has special meaning in various Haskell constructs, so it's best to avoid using it as an operator.

Let's create a custom operator `*+*` for the sum of squares function. To define it, we first declare its associativity and precedence, say left-associative and 6, followed by the definition:

```haskell
infixl 6 *+*

a *+* b = a ^ 2 + b ^ 2
```
Let's load it in the REPL, and indeed it works:

```
> 3 *+* 4
> 25
```

It can also be used in the functional style by enclosing it in parentheses:

```
> (*+*) 3 4
25
```

We could also define the operator in the prefix style:

```haskell
infixl 6 *+*

(*+*) a b = a ^ 2 + b ^ 2
```

#### Operator section

In Haskell, there's a special syntax for partially applying infix operators, called *section*:

```
> (2 /)
```

Here we bind the first (left) argument of the division operator with the value 2. Applying it to another number will give us:

```
> (2 /) 4
0.5
```

We can also bind the right argument, giving us a division by 2:

```
> (/ 2) 4
2
```

This is called *left section* and *right section*, respectively. To use the section, the operator and the value must be enclosed in parentheses. The only exception to this is the `-` operator, which will negate the number instead:

```
> (- 2)
-2
```

#### The `$` operator

Function application in Haskell is written with a space between the function name and its arguments, e.g. `f x`. We can instead think a custom operator `$` for function application:

```haskell
f $ x = f x
```

Such an operator already exists in the Haskell standard library, and it is used in the following manner:

```
> sin $ 0
0.0
```

This is equivalent to calling `sin 0`, so why do we need another operator? It turns out the `$` operator has the lowest possible precedence level (0), and it allows removing excess parentheses when using expressions with multiple functions. Suppose an expression:

```
> sin (pi / 2)
1.0
```

Without grouping `pi / 2` in parentheses, Haskell would first evaluate `sin pi` (due to the highest precedence of function application) and then apply `/ 2` to the result. Using the `$` operator we can *lower* the precedence level of function application, allowing first to calculate `pi / 2` and only then apply `sin` to the result:

```
> sin $ pi / 2
1.0
```

Moreover, the `$` operator is right-associative, which allows in most cases to remove parentheses from expressions on the right side. The following expressions are equivalent:

```
f (g x (h y)) == f $ g x (h y) == f $ g x $ h y
```

The `$` operator is used pervasively in Haskell code bases due to its usefulness.

### Base types

Haskell is a strong, statically-typed programming language. The term *strong* means that Haskell lacks implicit conversion between types, and *static* means that type checking is done during compilation, rather than the run time.

Haskell has strong *type inference*, allowing it to deduce (infer) the correct type of almost all expressions unless there's an error in the expression, in which case Haskell will report a type-checking error.

To learn the type of any expression in Haskell there exists the command `:type` (`:t` for short). Typing it, followed by an expression:

```
> :type 'c'
'c' :: Char
```

gives us the information that `'c'` is of type `Char`. The `::`, which can be read as "has type" or "is of type", is a typing operator, which binds the expressions ("terms") on the left with their type on the right. In most cases, type names in Haskell start with a capital letter.

The `Char` type includes all symbols of the alphabet, including Unicode symbols and control symbols, such as new line:

```
> :type '\n'
'\n' :: Char
```

However, if we enter in single quotes a non-char value, GHCi will report an error:

```
> :type 'zz'

<interactive>:1:1: error:
    • Syntax error on 'zz'
      Perhaps you intended to use TemplateHaskell or TemplateHaskellQuotes
    • In the Template Haskell quotation 'zz'
```

Another common type is `Bool`, which is inhabited by two values, `True` and `False`:

```
> :t True
True :: Bool
> :t False
False :: Bool
```

#### Numeric types

Haskell has a variety of numeric types, like `Int` (for 32/64 bit integers), `Integer` (arbitrary precision type, up to the limit of machine memory), as well as floating-point types like `Float` and `Double`.

All of these numeric types are members of the *type class* `Num` (we'll learn more about type classes in future modules). The type class mechanism in Haskell is used to provide a common "interface" for all numeric values, for example, the ability to add numbers using the same operator `+`.

Let's look at the type of some number literals in GHCi:

```
> :t 3
3 :: Num a => a
```

We can see that Haskell numbers are strangely defined: the type of the literal 3 is an arbitrary type `a`, which is prefixed with a certain *context* called `Num a`. We say that `a` is *constrained* by the `Num` type class.

However, we can also specify a concrete type when using literals. In this definition:

```
> x = 3 :: Int
> x
3
> :t x
x :: Int
```

We bind the identifier `x` with the `Int` value 3. We can also specify another type:

```
> y = 3 :: Double
> y
3.0
> :t y
y :: Double
```

This works because `Double` is also a member of the type class `Num`, allowing us to satisfy the constraint of the literal 3 in the context of `Double`.

Creating another value `z`, to which we add `Double` and `Int` values:

```
> z = y + 17
> :t z
z :: Double
```

This results in `Double` since the literal 17 is *polymorphic* in its return type, and since the `+` operator must return the same type as its arguments, we use the existing `Double` constraint of `y`, and the resulting type is `Double`.

As we've seen, whole numbers belong to the type class `Num`, while floating-point numbers belong to another type class, `Fractional`:

```
> :t 3.5
3.5 :: Fractional a => a
```

The `Float` and `Double` types belong to the `Fractional` type class, while `Int` and `Integer` do not.

The `Integer` type can inhabit any arbitrary-length integer value, limited only by the computer's memory. The `Int` type can be either 32- or 64-bit, depending on the architecture:

```
> 123456789012345678901234567890 :: Integer
123456789012345678901234567890
> 123456789012345678901234567890 :: Int

<interactive>:20:1: warning: [-Woverflowed-literals]
    Literal 123456789012345678901234567890 is out of the Int range -9223372036854775808..9223372036854775807
```

#### Function types

Function type signatures in Haskell are written with an infix arrow `->`, with the argument type on the left of the arrow, and the result type is on the right.

Haskell has a boolean `not` function, taking a boolean value and negates it. Let's see what it looks like in the REPL:

```
> not False
True
```

Since `not` is a function that takes a `Bool` type and returns a `Bool` type, its type signature is written as `Bool -> Bool`:

```
> :t not
not :: Bool -> Bool
```

In the case of two (or more) arguments, the type signature looks like this (using the binary `&&` (logical AND) function):

```
> (&&) False True
False
> :t (&&)
(&&) :: Bool -> Bool -> Bool
```

Recall that every function of *n* arguments in Haskell can be viewed as a function of 1 argument, returning another function of *n - 1* arguments. In this case, the function `&&` can be viewed as:

```
> ((&&) False) True
False
```

where `((&&) False)` is a partially applied function that expects one more `Bool` argument, making its return type a `Bool -> Bool` function. The complete expression can thus be written as `Bool -> (Bool -> Bool)`. The `->` operator is right-associative, so the parentheses can be removed, resulting in a type `Bool -> Bool -> Bool`.

We can view the rightmost parameter in the type signature as the return type, making all preceding parameters the argument types. Thus, `Bool -> Bool -> Bool` is read "a function of two `Bool` arguments, returning a `Bool`".

#### Importing functions

The standard Prelude contains many often-used functions, but not all. To gain access to other functions, defined in other modules, those modules first have to be *imported*.

Importing modules is done by using the keyword `import`, followed by the module name:

```haskell
module Demo where

import Data.Char
```

This gives us access to all functions exported by the module `Data.Char`, such as `isDigit`. Modules can also be imported directly in GHCi:

```
Prelude> import Data.Char
Prelude Data.Char> isDigit '7'
True
```

To find the module and name of specific functions, we can use [Hoogle](https://hoogle.haskell.org/) to look them up by name or type signature.

#### Tuples

Tuples are fixed-length couplings of arbitrary values, written in parentheses and separated by commas. The following syntax creates a tuple:

```
> (2,True) -- two-element tuple (also known as a pair)
(2,True)
> (2,True,'c') -- three-element tuple
(2,True,'c')
```

For pairs, there exist several helpful functions:

```
> fst (2,True) -- returns the first element of a pair
2
> snd (2,True) -- returns the second element
True
```

The type of a tuple consists of all types contained within the tuple:

```
> :t ('x',True)
('x',True) :: (Char, Bool)
```

Haskell does not have a single-value tuple, writing e.g. `(3)` is the same as writing the literal `3`. However, there's an "empty tuple" `()`, whose type is:

```
> :t ()
() :: ()
```

Here the value `()` and the type `()` are the same, but it is allowed since values and types exist in different namespaces.

#### Lists

Lists, like tuples, are containers of values. Unlike tuples, however, lists can only contain values of the same type (lists are so-called "homogenous", meaning all values must belong to the same type, versus "heterogeneous" tuples). Another difference is that the length of the list is not fixed and not known in compilation time. A list may also be empty.

Lists in Haskell are written in square brackets `[]`. Here's the syntax to create a list:

```
> [1,2,3]
[1,2,3]
> [False,True]
[False,True]
```

Since lists are homogenous, their type does not depend on their length. A type of a list of booleans is:

```
> :t [False,True]
[False,True] :: [Bool]
```

Here, the square brackets on the left specify the value of the list, and on the right is the type of the list, also placed in squared brackets. Here, `[Bool]` a list of `Bool` values.

For lists of type `[Char]` there exists a special syntax. A list of characters:

```
> ['H','i']
"Hi"
```

will be displayed as a String. The type of a list of characters is the same as the type of `String`. Haskell defines a `String` as a type alias of `[Char]`:

```
> :t ['H','i']
['H','i'] :: [Char]
> :t "Hi"
"Hi" :: [Char]
```

Lists are one of the most fundamental data types in Haskell and functional programming in general. We'll discuss operations on lists in future modules, but for now, we'll mention two of the most common operations: adding an element to the head of the list and concatenating two lists together.

To add (prepend) an element to the head of the list we use the `:` operator:

```
> str = 'H' : "ello"
> str
"Hello"
```

To append (concatenate) two lists together we use the `++` operator:

```
> str ++ " world"
"Hello world"
```

### Recursion

In imperative languages, the main tool for performing repetitive operations is a loop. In functional languages, loops are not meaningful, since those languages often lack the concept of a mutable variable, so it cannot be used to distinguish one loop iteration from the next.

In functional languages, repetition is done using recursion. The function is considered recursive if it contains in its right-hand side a call to the same function. Let's look at such a definition:

```haskell
factorial n = if n == 0 then 1 else n * factorial (n - 1)
```

Recursive functions must obey two rules in order not to get stuck in an infinite cycle:

1. calling a function recursively must be done on a value that differs from the input value of its formal parameter
2. there must exist a terminating condition to break the recursion

In our case we obey both rules: the recursive call to `factorial` is done on a value that's less than the input value `n`, and we have a conditional branch that does not result in a recursive call, allowing the function to terminate.

To visualize the way Haskell evaluates this expression we can use substitution to replace formal parameters with the actual values:

```
 factorial 2
  ~> if 2 == 0 then 1 else 2 * factorial 1
  ~> 2 * factorial 1
  ~> 2 * (if 1 == 0 then 1 else 1 * factorial 0)
  ~> 2 * factorial 0
  ~> 2 * (if 0 == 0 then 1 else 0 * factorial (-1))
  ~> 2 * 1
  ~> 2
```

Each reduction step consists of replacing any formal parameter with the result of this parameter. In this case, `n` has the value 2, initially, and each recursive call reduces the value by 1. Finally, we reach the condition where `n` is 0, and the recursion terminates, returning the value 1. It is multiplied by the initial value 2, resulting in 2 as the final result of this function.

#### Pattern matching

Using conditional expressions in Haskell is not always convenient. Haskell has a much more powerful mechanism for this purpose called *pattern matching*. The main idea is that the function is defined using not just one equation, but several, each describing a possible branch.

Rewriting `factorial` to use the pattern matching style:

```haskell
factorial' 0 = 1
factorial' n = n * factorial' (n - 1)
```

The new definition `factorial'` is written using two definitions. The difference between the two is how we describe function parameters. In the first definition, we bind the parameter not with a variable, but with a *possible* constant value. Here, 0 serves as a *pattern*, against which the value of `n` will be *matched*. If the match is successful, the function returns its value, otherwise, the next pattern will be tried. The second definition is called an *irrefutable* pattern - it can always be used to bind the parameter `n` with any value that is passed to it.

#### Errors and early termination

If a negative value is given to our `factorial` function, it will never reach the terminating condition (it will never *converge*) and will enter an endless loop (the program *diverges*). In the general case, this is unavoidable, since there are functions that are not defined for all arguments. However, hanging in an endless loop is the worst possible thing for the function to do. It would be better for the function to terminate and report an error to the diagnostic stream. There are two functions in the standard library to help deal with such errors - `error` and `undefined`.

The `error` function takes a `String` of text as an argument and prints an error with this text:

```
> error "ABC"
*** Exception: ABC
```

The `undefined` function does not take any arguments, it always terminates with an error message:

```
> undefined
*** Exception: Prelude.undefined
```

We can now augment the `factorial` function using one of these functions:

```haskell
factorial'' 0 = 1
factorial'' n = if n < 0 then error "arg must be >= 0" else n * factorial'' (n - 1)
```

Now calling this function with a negative number will terminate the program immediately with a helpful message.

Both `error` and `undefined` are useful when writing programs in Haskell. In Haskell's type semantics, both non-terminating recursion and early termination with an error are indistinguishable. In this case, it is considered that the return type of such programs is a special term called *bottom* (denoted by the mathematical symbol ⊥), which signifies a computation that never completes successfully. 

The bottom value is an element of all Haskell types, and the and `undefined` function provides a way to use this value. The `undefined` function can be substituted in place of any other expression in the program, and it is often used to mark yet unimplemented segments of code, but that the type checker accepts.

#### Guards

Sometimes, pattern matching is not a suitable syntax for dealing with complex conditions. Haskell contains another mechanism called *guards*, which allows better specifying conditions for handling specific cases. Let's rewrite `factorial` yet again, using the new syntax:

```haskell
factorial''' 0 = 1
factorial''' n | n < 0 = error "arg must be >= 0"
               | n > 0 = n * factorial''' (n - 1)
```

Here, the guard expressions allow specifying boolean conditions. If the guard condition is `True`, the right-hand expression is returned, otherwise, we continue to the next guard condition. If no guard conditions were satisfied, and there are no more conditions, the pattern matching fails with an error.

We can rewrite `factorial` using only guards in the following manner:

```haksell
factorial4 n | n == 0    = 1
             | n > 0     = n * factorial4 (n - 1)
             | otherwise = error "arg must be >= 0"
```

The function `otherwise` will always resolve to `True`, and we'll always reach it in case all other guard conditions were not satisfied.

#### Recursion with accumulation

If we wrote our factorial in C, we'd declare an accumulating variable holding an initial value, and would modify this variable in a loop, returning the accumulated value:

```c
long factorial (int n) {
  long acc = 1;
  while (n > 1)
    acc *= n--;
  return acc;
}
```

Haskell has no loops and no mutable variables, however, we can implement the same idea using an additional parameter:

```haskell
factorial5 n | n >= 0    = helper 1 n
             | otherwise = error "arg must be >= 0"

helper acc 0 = acc
helper acc n = helper (acc * n) (n - 1)
```

Our new definition is split into two parts: the definition of `factorial5`, which does argument checking, calling the helper function, and the `helper` function which has two parameters: an accumulator `acc` and the initial value `n`.

The `helper` function will on each recursive call decrease the value `n`, but also multiply its current value with the accumulator. Both conditions for recursion termination still hold: we're calling `helper` recursively with a different value `n`, and we have a terminating condition in the pattern match where `n` is 0.

In the case of the factorial function above, using the additional accumulator does not provide any extra benefits in Haskell, however, it is very often used to increase recursion efficiency and performance.

### Local Bindings

#### Significant whitespace

Haskell uses indentation for scoping. Haskell defines tabs to use 8 spaces, regardless of the configuration of your editor, and the use of spaces is encouraged.

Let's look at the function `roots` defined below:

```haskell
roots :: Double -> Double -> Double
          -> (Double, Double)
roots a b c =
  (
    (-b - sqrt (b ^ 2) - 4 * a * c)) / (2 * a)
  ,
    (-b + sqrt (b ^ 2) - 4 * a * c)) / (2 * a)
  )
```

The function definition here begins at indentation 0. On the first and 3<sup>rd</sup> lines we have a declaration of the type signature and the definition itself. The type signature is spread on two lines. The signature continues on the second line, and we could have broken it down further, as long as there's a non-zero indentation. Here is another example of a valid definition:

```haskell
roots :: Double
      -> Double 
      -> Double
      -> (Double -> Double)
```

Any line starting at indentation 0 means we are starting a new global definition. Inside the function body, any indentation can be arbitrarily used so long as the indentation remains above 0.

#### Removing duplication using `let .. in`

In the `roots` function above we repeat a sub-expression, namely `sqrt (b ^ 2) - 4 * a * c`, twice. To remove this duplication, we'd like to bind this sub-expression with a name and use this named expression instead.

Haskell includes a construct for such local bindings called `let .. in`. Here's another version of `roots`:

```haskell
roots' a b c =
  let d = sqrt (b ^ 2 - 4 * a * c) in
  ((-b - d) / (2 * a), (-b + d) / (2 * a))
```

The `let .. in` construct has two parts: the first part after the keyword `let` defines the local binding - an expression is bound to a value. In this case, the expression `sqrt (b ^ 2) - 4 * a * c` is bound to the name `d`. This name can now be used inside the `in` block, and indeed it is used twice. In this way, the `let .. in` construct helps to remove excess duplication.

Here's a simpler example in the REPL:

```
> let x = True in (True,x)
(True,True)
```

Here, we bound the value `True` to a local name `x` and used it inside the `in` block as a parameter to a tuple.

We can use more than one binding in the `let` block. Here's yet another version of `roots`:

```haskell
roots'' a b c =
  let d = sqrt (b ^ 2 - 4 * a * c)
      x1 = (-b - d) / (2 * a)
      x2 = (-b + d) / (2 * a)
  in  (x1, x2)
```

Here we can see the use of indentation to group bindings inside the `let` block. Each binding can refer to the next, regardless of the order in which they were defined. Here's one more change:

```haskell
roots''' a b c =
  let
    x1 = (-b - d) / aTwice
    x2 = (-b + d) / aTwice
    d  = sqrt (b ^ 2 - 4 * a * c)
    aTwice = a * 2
  in (x1, x2)
```

The only requirement that indentation inside the `let` block is on the same level, otherwise this can cause syntax and compilation errors.

The `let .. in` construct can also be used to define local functions. In the previous section we defined a function `factorial5` with the helper function:

```haskell
factorial5 n | n >= 0    = helper 1 n
             | otherwise = error "arg must be >= 0"

helper acc 0 = acc
helper acc n = helper (acc * n) (n - 1)
```

Here, since the helper function was defined at indentation 0, it is now available to all other functions, even though only the factorial function requires it, polluting the global namespace. We can move it inside the `let` block, and rewrite it as follows:

```haskell
factorial6 n
  | n >= 0 = let
      helper acc 0 = acc
      helper acc n = helper (acc * n) (n - 1)
    in helper 1 n
  | otherwise = error "arg must be >= 0"
```

Again, the only requirement here is keeping the indentation consistent.

We can also use `let .. in` to create a pattern. Suppose a function `rootsDiff`:

```haskell
rootsDiff a b c = let
  (x1,x2) = roots a b c
  in x2 - x1
```

Here, instead of calling the `roots` function, later using the functions `fst` and `snd` to project the first and second values out of the pair, we use the `let` block to deconstruct the pair by using pattern matching, binding both pair values to the names `x1` and `x2`.

#### Binding using `where`

The `where` construct is similar to `let .. in`, except it works in the opposite - if `let .. in` allows us to declare bindings up front, and later use them, by using `where` we first specify the resulting expression, and only later specify the bindings.

```haskell
roots'''' a b c = (x1, x2) where
  x1 = (-b - d) / aTwice
  x2 = (-b + d) / aTwice
  d  = sqrt $ b ^ 2 - 4 * a * c
  aTwice = a * 2
```

Here we first declare the resulting pair `(x1, x2)`, followed by the `where` keyword, after which we declare all bindings.

The main difference between `let .. in` and `where`, other than the order, is the fact that `let .. in` is itself an expression that can be used in other expressions, while `where` is not an expression:

```
> let x = 2 in x ^ 2
4
> (let x = 2 in x ^ 2) ^ 2
16
> x ^ 2 where x = 2

<interactive>:28:7: error: parse error on input ‘where’
```

The `where` keyword can only be used inside a function definition and only in a specific place. This makes it suitable in cases where using the `let .. in` is not possible. Recall the last definition of `factorial6`:

```haskell
factorial6 n
  | n >= 0 = let
      helper acc 0 = acc
      helper acc n = helper (acc * n) (n - 1)
    in helper 1 n
  | otherwise = error "arg must be >= 0"
```

Suppose we wanted to use the `helper` function not only in the first guard but also in other guard expressions. Because of the different guards, the entire body of `factorial6` is no longer a single expression. This is where the `where` style may become useful, allowing us to declare a common binding for all individual guard clauses:

```haskell
factorial7 :: Integer -> Integer
factorial7 n | n >= 0    = helper 1 n
             | otherwise = error "arg must be >= 0"
  where
    helper acc 0 = acc
    helper acc n = helper (acc * n) (n - 1)
```

Even though we're not using the `helper` function in the `otherwise` case, it's still available if we need it.