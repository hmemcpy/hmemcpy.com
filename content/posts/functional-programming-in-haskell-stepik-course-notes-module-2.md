+++
title = "Functional Programming in Haskell (Stepik course notes) - module 2"
date = 2020-01-20T23:07:38Z
+++
This is the second module (out of 5) of my English summary of the Haskell MOOC on Stepik, available only in Russian. Read the first part in the *Introduction* module.

1. [Introduction](/posts/functional-programming-in-haskell-stepik-course-notes-module-1/)
2. **Programming fundamentals** (this page)
3. Lists
4. Data types
5. Monads

<!-- more -->

## Programming fundamentals

### Parametric polymorphism

A function is said to be *polymorphic* if it can be used on values of different types. For example, the `+` operator may be used on values of type `Int`, returning an `Int` value, or `Double` values, returning a `Double`. This makes `+` a polymorphic operator.

There are two kinds of polymorphism: *parametric polymorphism* and *ad hoc polymorphism*. The former means that the function implementation is identical for all types which this function can be used with, the latter implies that for each type used with this function, there exists a special implementation, specific to the type. The examples above, using the `+` operator with `Int` and `Double` types, are examples of ad hoc polymorphism, since the implementation of addition for those types behaves differently.

#### Polymorphic functions

The simplest example of a polymorphic function is `id` (which exists in the standard library), which returns its argument:

```
> id x = x
> :t id
id :: t -> t
```

This function's type is `t -> t`. Here, `t` is called a *type variable*, meaning it can be applied to any arbitrary type. In Haskell, concrete types (such as `Integer`) start with a capital letter, and type variables start with a lowercase letter.

This function is parametrically polymorphic since there are no further restrictions on the input parameter - it is returned unchanged from the function. We can call this function on values of arbitrary types:

```
> id True
True
> id 5
5
```

We can also call `id` on the function `id` itself. The result is the function `id` itself, which can be further applied to any value:

```
> (id id) 4
4
```

The type of a fully applied polymorphic function, e.g. `id True`, is a `Bool` type:

```
> :t id True
id True :: Bool
```

What is the type of `(id id)`? The function itself is passed as an argument, making the return type the same type as the argument, namely `t -> t`:

```
> :t (id id)
(id id) :: t -> t
```

Let's define a two-argument function `k` with parameters `x` and `y`. Not knowing anything about `x` and `y`, the only thing we can do here is return either `x` or `y`. Let's return `x`:

```
> k x y = x
```

We'll get a function that always ignores its second argument, always returning the first:

```
> k 42 True
42
> k 42 55
42
```

The type of our function `k` is:

```
> :t k
k :: t1 -> t -> t1
```

Here we see the use of type variables `t1` and `t`, meaning that the actual types are not important, `t1` and `t` could be different types. The return value is the first argument `t1`. This function already exists in the standard library, and it's called `const`. The `const` function always returns its first argument, ignoring the second. Here's the signature of `const`:

```
> :t const
const :: a -> b -> a
```

This type is using different names for its type variables, but it is identical to our `k` function.

If we partially apply `const` to one argument, e.g. `const True`, its type is:

```
> :t const True
const True :: b -> Bool
```

This partially-applied `const` can accept any arbitrary value, ignore it, and will always return a `Bool` value, namely `True`.

In the previous module, we talked about the `error` and `undefined` functions, which immediately halt the execution, printing an error message:

```
> undefined
*** Exception: Prelude.undefined
> error "boom"
*** Exception: "boom"
```

The type of `undefined` is also parametrically polymorphic:

```
> :t undefined
undefined :: a
```

The `undefined` function has a type variable `a`, which means it can be substituted for any type. It can be written anywhere an arbitrary type is expected, and it will still be correctly type-checked.  The `error` function, when given an error message, also inhabits all types:

```
> :t error "boom
error "boom" :: a
> :t error
error :: [Char] -> a
```

The `undefined` and `error` functions in Haskell halt program execution, which is why it's possible to define them using the highest (unconstrained) level of polymorphism, namely an arbitrary type parameter. Without any additional context, it's impossible to create a value of type `a`, so the only thing these functions can do is either hang forever or terminate with an error message. Those functions are called *bottom* values and denoted with a mathematical symbol ⊥.

#### Most general type

We can limit function polymorphism by explicitly specifying its type. Consider an example:

```haskell
mono :: Char -> Char
mono x = x

semiMono :: Char -> a -> Char
semiMono x y = x
```

The implementation of the `mono` function above does not differ from the implementation of `id`, however, we specified that it can only be applied to values of type `Char`. Calling it with a `Char` value will return the value, otherwise, it will cause an error:

```
> mono 'x'
'x'
> mono True

<interactive>:1:6: error:
    • Couldn't match expected type ‘Char’ with actual type ‘Bool’
    • In the first argument of ‘mono’, namely ‘True’
      In the expression: mono True
      In an equation for ‘it’: it = mono True
```

A function that operates on concrete types is called a *monomorphic* function.

We can partially limit polymorphism, demonstrated by the function `semiMono`. It is a two-argument function, with an arbitrary second parameter.

If we do not explicitly specify the function type, Haskell will infer the *most general type* available for the function. If we comment out the `semiMono :: Char -> a -> Char` declaration above, Haskell will infer the following type for `semiMono`:

```
> :t semiMono
semiMono :: t1 -> t -> t1
```

The type inference algorithm that Haskell uses is based on the [Hindley-Damas-Milner](https://en.wikipedia.org/wiki/Hindley%E2%80%93Milner_type_system) algorithm. This algorithm infers the most general type for any given expression. If an expression has no further restrictions, Haskell infers a generic type variable, otherwise, it will infer a monomorphised type parameter, such as `Char` in the example above.

#### Higher-order functions

A *higher-order function* is a function that takes another function as an argument. In Haskell and other functional languages, higher-order functions are used pervasively. We've already encountered one such function, the `$` operator, the low-precedence function application operator.

Let's look at the type of the `$` operator:

```
> :t ($)
($) :: (a -> b) -> a -> b
```

It is a polymorphic type, a function of two arguments. Its first argument (left) is a function, the second argument (right) is a value of an arbitrary type. The `$` operator applies its left argument to the right. This requires the types to match - the type of the right argument `a` must match the type of the input parameter of the left argument `a -> b`. The result of the `$` operator is the result of the left argument function. Since the result of `a -> b` is the type `b`, it is the resulting type of applying `$` operator.

Let's look at another example. Suppose the function `apply2` which applies the function twice:

```
> apply2 f x = f (f x)
```

What is the type of this expression? If we look at the above definition of `f`, it's a function from `a -> b`. The inner `(f x)`, therefore, results in a type `b`. But now the outer function `f` is applied to the result of `(f x)`, which is `b`, however, it expects `a -> b`? How can this be, if this function compiles just fine?

Since both types `a` and `b` of our function `f :: a -> b` are completely arbitrary, the type checker can infer that in this case, the types `a` and `b` are the same. Applying a function `a -> b` on a value of type `b` only works if `a` and `b` are the same type.

The Haskell compiler understands this, and it's able to monomorphise the function to the following signature:

```
> :t apply2
apply2 :: (t -> t) -> t -> t
```

Making the first argument, `f`, a function where the input and output types are the same. The second argument, `x` is a value of the same type, which is also the return type of the `apply2` function. This means our `apply2` function can be used on fewer types of values than `$`.

```
> apply2 (+5) 22
32
> apply2 (++"AB") "CD"
"CDABAB"
```

Here we see the function `apply2` used with values of the same type: the first applies the function `(+5)` twice to the integer 22, and the second appends the string "AB" twice to the string "CD".

Now let's look at a more useful function from the standard library, `flip`:

```
flip f y x = f x y
```

This function has 3 parameters: the function `f`, and two additional parameters `y` and `x`. It ends up applying the function `f` to the parameters in the reversed order, flipping between `y` and `x`. Here's an example using division:

```
> (/) 4 2
2.0
> flip (/) 4 2
0.5
```

Here, because `flip` switches the order of parameters, we get `2 / 4` instead of `4 / 2`, resulting in 0.5.

Let's see what happens when `flip` is applied to the function `const`. As you may recall, the `const` function always returns the first argument, ignoring the second. By flipping the arguments, `flip const` is now a function that always returns the second argument, ignoring the first!

```
> flip const 5 True
True
```

The `flip` function has the following type:

```
> :t flip
flip :: (a -> b -> c) -> b -> a -> c
```

Recall that in Haskell, any function can be considered a function of one argument, returning another function. In this case we can see that `flip` is a function that accepts a two-argument function `(a -> b -> c)` and returns a function `(b -> a -> c)` with the arguments reversed.

We can see from the type of `flip const` that it takes two arguments, and always returns the second:

```
> :t flip const
flip const :: b -> c -> c
```

#### Anonymous functions - Lambda

In Haskell, similar to mathematics, functions have names, and we apply the function by calling its name. However, there's an alternative - *anonymous functions*. Consider the expression:

```
2 * x + 7
```

This expression contains an unknown variable `x`, and cannot be used in this form as a bound expression:

```
> 2 * x + 7

<interactive>:2:5: error: Variable not in scope: x
```

To compute the expression for any given `x` we usually resort to declaring a function that takes an `x` as an argument:

```
> f x = 2 * x + 7
```

Now it's a regular function that can be applied to any `x`, e.g.:

```
> f 10
27
```

However, instead of creating a named function, we can bind the value `x` using a *lambda expression*, by using the following syntax:

```
> \x -> 2 * x + 7
```

We start by writing a backslash symbol (`\`), followed by the variable `x`, followed by an arrow `->`, after which we can refer to `x` in the body of the expression. The character `\` was chosen because it visually resembles the Greek letter lambda (λ).

This creates an anonymous function (also called a lambda function or lambda expression), which behaves exactly like the named function `f` above. We can use this expression to apply it to the same value:

```
> (\x -> 2 * x + 7) 10
27
```

We can define another function, `f'`, binding it to the lambda expression:

```
> f' = \x -> 2 * x + 7
> f' 10
27
```

Using those definitions, both `f` and `f'` are equivalent.

We can pass multiple arguments to the lambda expression. Consider a function `lenVec` which calculates vector length:

```
> lenVec x y = sqrt $ x^2 + y^2
> lenVec 3 4
5.0
```

We can rewrite this function as a series of lambda expressions, by moving the formal parameters to the right-hand side, turning them into lambda parameters:

```
> lenVec = \x -> \y -> sqrt $ x^2 + y^2
```

Haskell has a convenient syntactic sugar for specifying lambdas with multiple parameters:

```
> lenVec = \x y -> sqrt $ x^2 + y^2
> lenVec 3 4
5.0
```

Anonymous functions are most commonly used when using higher-order functions. Recall that a higher-order function is a function that accepts another function as an argument. Consider the following example:

```
> p1 = ((1,2), (3,4))
> p2 = ((3,4), (5,6))
```

Here, `p1` and `p2` are pairs of pairs. Let's write a function that sums the first elements of each pair. To get the first element of the first pair we could use the function `fst` twice, like so:

```
> fst $ fst p1
1
```

Let's now use it in a function that looks like this:

```haskell
import Data.Functions

sumFstFst = (+) `on` helper
    where helper pp = fst $ fst pp
```

The `on` function is defined in the `Data.Functions` module, and has the following signature:

```
on :: (b -> b -> c) -> (a -> b) -> a -> a -> c
on op f x y = f x `op` f y
```

It is used to run a binary function `op` on the results of applying the unary function `f` to two arguments `x` and `y`. It can be used, for example, to define the `sumSquares` function from the previous module:

```
sumSquares = (+) `on` (^2)
```

The `x` and `y` arguments here are omitted. Following the definition of `on`, substituting the values, we get:

```
(^2) x + (^2) y
  
  ^    ^   ^
  |    |   |
  |    |   +-- f
  |    +------ op
  +----------- f
```

Our `sumFstFst` is a function of two arguments. We apply the operator `+` to the result of applying `helper` to both arguments:

```
> sumFstFst p1 p2
4
```

Visualized as the following:

```
((+) `on` helper) p1 p2
 ~> helper p1 + helper p2
 ~> fst $ fst p1 + fst $ fst p2
 ~> 1 + 3
 ~> 4
```

It extracts the first element from `p1`, which is 1, the first element from `p2` which is 3, giving us the desired result 4.

This works, but we would like to avoid declaring the named `helper` function, so we can use a lambda expression instead, omitting the `where` clause entirely:

```
sumFstFst' = (+) `on` (\pp -> fst $ fst pp)
```

### Parametric polymorphism (2)

Suppose we have two polymorphic functions, `f` and `g`. We would like to create a composite function, that takes both functions `f` and `g`, and applies them to the argument `x` in the following manner: first, apply `g` to `x`, and then apply `f` to the result. Let's look at how we can define such a composition operator.

#### Function composition

Suppose our `f` and `g` functions have the following signatures:

```
f :: b -> c
g :: a -> b
```

Also, we have an argument `x` of type `a`:

```
x :: a
```

To apply the function `f` to the result of applying `g`, the result type of `g` must be the same as the input type of `f`, namely `b`. The function `g` accepts an argument of type `a`:

```
f (g x)
```

This gives us a result of type `c`, but we want instead to get a composite function from `a -> c`.

We can achieve this by abstracting over `x` using a lambda expression:

```
\x -> f (g x)
```

And this gives us the expected result, a function `a -> c`.

The complete composition function, therefore, can be defined thus:

```
compose f g = \x -> f (g x)
```

This operator already exists in Haskell, and it is called `.`. Its type is:

```
> :i (.)
(.) :: (b -> c) -> (a -> b) -> a -> c 	-- Defined in ‘GHC.Base’
infixr 9 .
```

Which is precisely what we wanted: it takes a function `b -> c`, another function `a -> b`, and returns a composite function `a -> c`.

Note the use of `:i` (short for `:info`) in GHCi - it returns additional information about the definition, such as where it is defined and its fixity, if available.

Now let's look at how we can use this operator. In the previous section, we defined a function `sumFstFst'`:

```
sumFstFst = (+) `on` (\pp -> fst $ fst pp)
```

In the lambda expression that extracts the first element from a pair of pairs, we used the `fst` function twice, to first extract the first pair, and then extract the first element from that pair. We are applying the function `fst` to the result of applying `fst` to the argument `pp`, and this is exactly what the composition operator gives us, allowing us to simplify the expression to the following:

```
sumFstFst'' = (+) `on` (fst . fst)
```

The function `(fst . fst)` is a more compact equivalent of `(\pp -> fst $ fst pp)`, called the *point-free* style, allowing us to omit the argument. Chains of function applications can be rewritten to this style:

```
doIt x = f (g (h x)) == f ((g . h) x) == (f . (g . h)) x
```

Allowing us to drop the argument `x` on both sides, giving us:

```
doIt = f . g . h
```

#### Tuple and list polymorphism

Until now, when talking about parametric polymorphism, we used functions. However, built-in Haskell types, such as tuples and lists are also parametrically polymorphic. Let's start with a list. Suppose we have a list of `Bool` values:

```
> :t [True,False]
[True,False] :: [Bool]
```

A list in Haskell is written by using square brackets `[]`, and its type is polymorphic, depending on the type of its elements. Since lists are homogeneous, they can only contain values of the same type.

If we look at the type of an empty list:

```
> :t []
[] :: [a]
```

We'll see that its type is a type variable `a`, meaning the list is polymorphic in its elements.

This is also apparent from functions that operate on lists, such as the concatenation operator `++`, taking two lists of the same type and produces another list of the same type:

```
> :t (++)
(++) :: [a] -> [a] -> [a]
```

Similar to the `:` operator that adds an element to the head of the list:

```
> :t (:)
(:) :: a -> [a] -> [a]
```

Tuples in Haskell are also polymorphic. Let's recall the syntax of creating a tuple:

```
> (True,3)
(True,3)
```

However, there's an alternative syntax for creating a tuple. Instead of specifying the values inside the tuple braces, we can use it in a prefix style:

```
> (,) True 3
(True,3)
```

The first syntax is called a *mixfix* style, where the values are mixed with the tuple structure. The prefix style can be used to create tuples of any length, e.g.:

```
> (,,) True 3 'c'
(True,3,'c')
```

Let's look at the types of tuple construction operators:

```
> :t (,)
(,) :: a -> b -> (a, b)
> :t (,,)
(,,) :: a -> b -> c -> (a, b, c)
```

The type variables can be substituted for any type. We can also partially-apply the tuple operator, resulting in:

```
> :t (,,) True 'x'
(,,) True 'x' :: c -> (Bool, Char, c)
```

We can create a function that turns a single value into a pair, with the value duplicated:

```
> dup x = (x,x)
> :t dup
dup :: t -> (t, t)
```

Since there are no constraints on the value `x`, the Haskell compiler infers a type variable `t`, meaning that the input and the first and second elements of the resulting pair must be the same type.

The projection functions `fst` and `snd` that we encountered earlier have the types:

```
> :t fst
fst :: (a, b) -> a
> :t snd
snd :: (a, b) -> b
```

Resulting in `fst` to return the first element `a`, ignoring the second, and `snd` does the opposite - returns the second element `b`, ignoring the first.

#### Currying

In most programming languages, function calls are made by specifying the function name, followed by parentheses, followed by a list of arguments, separated with a comma, e.g. `max(3, 7)`.

In Haskell, function application is done without any additional punctuation, but by specifying the arguments after the function name with a space between them: `max 3 7`. Haskell allows us to not specify all the arguments to the function, resulting in a partially-applied function that can later be passed the rest of the arguments.

This technique of turning an *n* argument function into a sequence of functions accepting one argument is called *currying*, named after a logician Haskell Curry, who formalized it after it was discovered by a Russian mathematician Moses Schönfinkel. The Haskell language is named after Haskell Curry.

However, not all functions in Haskell are curried. Functions that operate on tuples bare resemblance to function calls in imperative languages, i.e. `fst (1, 2)`. To move between curried and uncurried forms, we can use two combinators, `curry` and `uncurry`. Let's look at a few examples:

Recall the function `on` we learned in the previous section. It takes 4 parameters, the first being a function of two arguments:

```
> :t on
on :: (b -> b -> c) -> (a -> b) -> a -> a -> c
```

In other words, the first expected argument `(b -> b -> c)` is a *curried* function. If we try to use a function `fst` as the first argument, we will get a type error, saying the types don't match - our `fst` function is the wrong shape - it is an *uncurried* function `(a, b) -> a`:

```
> :t fst `on` (^2)

<interactive>:1:1: error:
    • Occurs check: cannot construct the infinite type:
        b ~ (b -> c, b0)
      Expected type: b -> b -> c
        Actual type: (b -> c, b0) -> b -> c
    • In the first argument of ‘on’, namely ‘fst’
      In the expression: fst `on` (^ 2)
```

To turn an uncurried function into a curried one, we can use the `curry` combinator that does just that:

```
> :t curry fst
curry fst :: a -> b -> a
```

turning the `fst` function into the correct shape to use with the `on` function:

```
> :t curry fst `on` (^2)
curry fst `on` (^2) :: Num c => c -> c -> c
```

Let's define another function `avg` that averages the values of a pair:

```haskell
avg :: (Double,Double) -> Double
avg p = (fst p + snd p) / 2
```

This is another example of an uncurried function, and if we want to use it with a higher-order function, such as `on`, we need to turn it into a curried one, using `curry`:

```
> :t curry avg `on` (^2)
curry avg `on` (^2) :: Double -> Double -> Double
```

How would we define the `curry` function ourselves? Let's define a function `curry'` with the arguments:

```
curry' f x y = ...
```

The `curry'` function expects a function `f` to operate on a tuple. To do this, we need to turn our arguments `x` and `y` into a tuple, resulting in:

```
> curry' f x y = f (x,y)
```

Looking at the inferred type signature we can see that it does exactly what is expected:

```
> :t curry'
curry' :: ((a, b) -> c) -> a -> b -> c
```

it takes an uncurried function `(a, b) -> c`, giving us back a curried function `a -> b -> c`. 

This signature matches exactly the definition of `curry` from the standard library.

The opposite operation is called `uncurry`, a function that takes a curried function and returns a function that operates on a pair:

```
> :t uncurry
uncurry :: (a -> b -> c) -> (a, b) -> c
```

### Type classes

In the previous section, we learned about parametric polymorphism. A function is polymorphic if it can be applied to arbitrary types, without any additional restrictions. This section talks about a specialized, *ad hoc polymorphism*. A function can be still applied to arguments of various types, as long as those types provide an implementation of an interface that defines the specialized behavior. This type of interface in Haskell is called a *type class*, and its implementations are called *instances*.

#### Contexts

Numeric constants in Haskell have the following representation:

```
> :t 7
7 :: Num a => a
```

Whenever we encounter a "fat arrow" (sometimes called an *implication*) in the type signature, it splits the type into two parts: on the right-hand side is the type of the expression (in this case we say that 7 has the type `a`), and on the left-hand side we have a so-called *context*. The context contains two parts: the name of the *interface* that the type must provide an implementation for, and the type parameter for which this interface is defined. In our case, we say that 7 has a polymorphic type `a`, but this type `a` must have an implementation for the interface `Num`.

We will use the terms *type class* instead of "interface", and *instance* instead of "implementation".

The type class `Num` contains a series of operations on numbers, such as *addition*, *multiplication*, and others.

Looking at the definition of the addition operator `+`:

```
> :t (+)
(+) :: Num a => a -> a -> a
```

we see that it is also a polymorphic function that takes two arguments of the same type `a`, returning an argument of type `a`, provided the type `a` has an instance of `Num` (we can also say "belongs to the `Num` type class", or "members of the `Num` type class").

There are many different type classes, providing various behaviors, such as comparison. The operator `>` (greater than) has the following definition:

```
> :t (>)
(>) :: Ord a => a -> a -> Bool
```

It takes two arguments of the same type and returns a boolean value, indicating whether the first argument is greater than the second. The type `a` must belong to the type class `Ord` which defines this behavior.

Let's see what happens when we partially-apply the `>` operator with a number, e.g.:

```
> :t (> 7)
(> 7) :: (Num a, Ord a) => a -> Bool
```

Due to the operator section, `(> 7)` becomes a unary predicate of type `a -> Bool`, however, its context has expanded: it is now required that the type `a` belongs to both `Num` and `Ord` type classes - the `Ord` constraint due to the use of `>`, and the `Num` constraint due to the use of a numeric value 7.

A slightly more complicated example is using the operator section on a pair:

```
> :t (> (1,2))
(> (1,2)) :: (Num t, Num t1, Ord t, Ord t1) => (t, t1) -> Bool
```

Pairs are also members of the `Ord` type class if the elements of the pair are members of that type class. Pair elements can be of different types, evident here by the use of `t` and `t1` type variables. Both types have constraints of belonging to the `Num` and `Ord` type classes.

Now that we know how to read type class constraints, we can tell more about the errors that happen in case Haskell cannot satisfy such constraints. Consider the example:

```
> :t (* 'c')

<interactive>:1:2: error:
    • No instance for (Num Char) arising from a use of ‘*’
    • In the expression: (* 'c')
```

We are trying to use the multiplication operator `*` with a character value `'c'`. Here, Haskell reports and error that there are no instances of type class `Num` (which `*` requires) for the type `Char`. We could fix this by defining our own instance of `Num Char`, providing we could implement such behavior.

#### Type class declaration

A type class provides an interface which can be implemented for concrete types. The type class declaration is a collection of named functions, having certain signatures. Here's an example:

```haskell
class Eq a where
  (==) :: a -> a -> Bool
  (/=) :: a -> a -> Bool
```

A type class is defined by starting with the keyword `class`, followed by the name of the type class, followed by the type parameter for which this type class can be defined. After which, the keyword `where`, followed by the functions the type class instance must implement. The function definitions must start at the next indentation level.

In our case, `Eq` can be defined for any arbitrary type `a`. Each instance of `Eq` will replace `a` with the concrete type for which it is implemented. The two functions defined in the interface, namely `==` and `/=` check for equality and inequality, respectively. Both have the signature `a -> a -> Bool`.

The `Eq` type class is already defined in the Haskell standard library. Let's look at how it is used:

```
> :t (==)
(==) :: Eq a => a -> a -> Bool
```

The equality operator is a polymorphic function with a constraint that type `a` must be a member of `Eq`. This constraint remains as long as the values themselves remain polymorphic. In the expression:

```
> :t (== 42)
(== 42) :: (Eq a, Num a) => a -> Bool
```

We can see that operator section, applied to a polymorphic value (recall that numbers in Haskell are polymorphic with a `Num` constraint), we can see that the `Eq` requirement remains, but also the `Num` requirement was added, meaning that the remaining argument must be a member of both `Eq` and `Num` type classes.

If we partially apply the operator to a concrete type, e.g. `Char`:

```
> :t (== 'x')
(== 'x') :: Char -> Bool
```

we see that the `Eq` requirement was removed, as Haskell monomorphised this expression to the concrete `Char` type.

Let's now look at a few functions that use the `Eq` constraint. One such function, `elem` from the standard library, checks whether the value is an element in a list:

```
> :t elem
elem :: Eq a => a -> [a] -> Bool
```

The arguments to `elem` is the value we're checking, as well as the list of those values. It works by equating the value with each element in the list, returning `True` in case such element was found, otherwise `False`. In order to perform such an equality check, the type `a` must be a member of the `Eq` type class.

Reading type class constraints on type signatures is a powerful reasoning mechanism in Haskell, allowing us to deduce a lot about how a function behaves just from reading the type signature, without looking at the implementation.

#### Type class instances

A type is considered a member of a type class, if there exists an implementation (called *instance*), implementing that type class. Here's an example:

```haskell
class Eq a where
  (==), (/=) :: a -> a -> Bool

instance Eq Bool where
  True   == True  = True
  False  == False = True
  _      == _     = False

  x /= y  = not (x == y)
```

The `Eq` definition has two functions, checking for equality and inequality. Here we are using a more compact style of writing, as both functions have the same signature, Haskell allows placing them in a single line, separated by commas.

To declare a type class instance, we use the `instance` keyword, followed by the type class name, followed by the type for which we implement this instance (`Bool` in this case, causing our function signatures to monomorphise to `Bool -> Bool -> Bool`). This is followed by the keyword `where`. The next line (and the next indentation level) defines the implementations of the functions. In this case we use pattern matching to define the first signature, `==`.

Boolean equality defined such that `True` is always equal to `True`, and `False` is always equal to `False`. Any other permutation is not equal, denoted here by using a placeholder symbol `_`, which in Haskell can be read as "in all other cases". Here it means that the match will always be successful, if the previous two failed, and the result will always be `False`, regardless of the values that were matched.

The next implementation is the inequality function `/=`. In this case, we implement it via the equality implementation, negating the result of `==` with the function `not`. In such cases, where a function can be implemented in terms of another, it can be defined in the type class definition itself:

```haskell
class Eq a where
  (==), (/=) :: a -> a -> Bool
  x /= y  = not (x == y)
```

In such cases, it's often enough to implement just the functions that don't already have a default implementation. It is also possible to define cyclic implementations:

```haskell
class Eq a where
  (==), (/=) :: a -> a -> Bool
  x /= y  = not (x == y)
  x == y  = not (x /= y)
```

Since GHC 7.8.1, Type classes may state a [*minimal complete definition*](https://downloads.haskell.org/~ghc/7.8.1-rc1/docs/html/users_guide/pragmas.html#minimal-pragma), a specification of which minimal set of functions must be implemented by all instances.

#### Polymorphic instances

We can also define type class instances for polymorphic types. For example, an `Eq` instance for a two element tuple (a pair). Two pairs are equal if their elements are equal. Pair elements themselves must be members of the `Eq` type class:

```haskell
instance (Eq a, Eq b) => Eq (a, b) where
  p1 == p2 = fst p1 == fst p2 && snd p1 == snd p2
```

Here we implement an instance for a polymorphic `Eq (a, b)`, with the additional constraint that `a` and `b` themselves must have an instance of `Eq`, as evident by the declaration `(Eq a, Eq b)` on the left-hand side of the `=>` sign, allowing us to use the equality `==` operator in the expression body. No need to place each part in parentheses, since `==` has higher precedence than `&&`.

Similarly, we can define an instance for lists:

```haskell
instance Eq a => Eq [a] where
  ...
```

All the definitions above already exist in the standard library, as well as many others, implementing all common base types.

Not all types can be checked for equality. In Haskell, there are functional types for which implementing such equality is not possible. Consider the example:

```
> id == (\x -> x)

<interactive>:1:1: error:
    • No instance for (Eq (a0 -> a0)) arising from a use of ‘==’
        (maybe you haven't applied a function to enough arguments?)
    • In the expression: id == (\ x -> x)
```

Even though as implementors we know in this case that those two functions are identical, from theoretical computer science, function equality is said to be *undecidable* in a Turing-complete language, therefore it's not possible to implement in Haskell. Here, Haskell reports an error that there's no instance of `Eq` for a function type `a0 -> a0`.

### Standard type classes

In this section we'll talk about *type class extension*. This is similar to extension in object-oriented languages, however in Haskell we are extending the type class interfaces, never implementations.

#### Class extensions

Let's consider an example of the `Ord` type class (also exists in the standard library):

```haskell
class Eq a where
  (==), (/=) :: a -> a -> Bool
  x /= y  = not (x == y)
  x == y  = not (x /= y)

class (Eq a) => Ord a where
  (<), (<=), (>=), (>) :: a -> a -> Bool
  max, min :: a -> a -> a
  compare :: a -> a -> Ordering
{- Minimal complete definition: either compare or <= -}
```

The `Ord` type class is parameterized by `a` and itself has a *context* of `Eq a`. When placing such context in the type class definition (rather than the instance), it means that the `Ord` type class *extends* the `Eq` type class. In order to define an instance of `Ord` we must first define an instance `Eq`.

The `Ord` type class defines the ordering behavior used in comparisons. Other than the usual ordering operators `<`, `<=`, `>=`, and `>`, we can define the `max` and `min` functions, as well as a function `compare`, which can be used for a more detailed comparison. The `compare` function returns a result `Ordering`, which is a type consisting of 3 values: LT, EQ, and GT (less than, equals, and greater than):

```
Prelude> :i Ordering
data Ordering = LT | EQ | GT 	-- Defined in ‘GHC.Types’
...
```

In the minimal complete definition of the `Ord` type class it is stated that a valid instance can be defined by only implementing either the `compare` or `<=` functions.

We can also do a sort of *multiple inheritance*, by specifying several interfaces that extend our type class, e.g.:

```
class (Eq a, Printable a) => MyClass a where
  ...
```

Since in Haskell we're extending the type class interfaces themselves, and not the implementations, problems such as multiple inheritance in object-oriented languages do not occur.

#### `Show` and `Read`

The standard library contains a useful type class `Show` with a function `show`, which can be used to create a string representation of a value.

First, let's see how the `show` function is defined:

```
> :t show
show :: Show a => a -> String
```

It takes any arbitrary type `a` and returns a String, provided our `a` is a member of `Show`:

```
> show 5
"5"
> show 5.0
"5.0"
> show [1,2]
"[1,2]"
```

If `Show` performs a sort of a serialization of a value to `String`, the type class `Read` performs the opposite operation: it reads an arbitrary `String` value, and returns a type `a`, if an instance of `Read` exists for `a`:

```
> :t read
read :: Read a => String -> a
```

However, if we attempt to use it as-is, we'll get the following error:

```
> read "5"
*** Exception: Prelude.read: no parse
```

(in older versions of GHC this would print a large message about a missing instance `(Read a0)`)

Why did we get an error?

Our `read` function is polymorphic in its return type, and here we must explicitly specify the return type of the function. Otherwise, Haskell has no way of knowing whether the string constant `"5"` is an `Int`, `Double`, or something else. To use the `read` function properly we must specify the return type using the syntax:

```
> read "5" :: Int
5
> read "5" :: Double
5.0
> read "[1,2]" :: [Double]
[1.0,2.0]
```

The `read` function is not defined in the `Read` type class, because it has limited usefulness. In case it is unable to parse the input value, it will return an error. Suppose we attempt reading the string "5 rings" as an `Int`:

```
> read "5 rings" :: Int
*** Exception: Prelude.read: no parse
```

It will fail, because it won't be able to read the entire string. For this reason, there exists a function `reads`, which is a safer version that is able to return unparsed elements as a pair, in addition to the parsed value:

```
> reads "5 rings" :: [(Int,String)]
[(5," rings")]
```

Returning the successful `Int` value as the first element, and the remainder string as the second element.

#### `Enum` and `Bounded`

Many types are considered *enumerations*, as if their values can be listed with a comma. For example, the `Int` values can be listed as "1,2,3...". Each element can be less then or greater than its predecessor, and we can move up and down the type by increasing or decreasing the value. Same goes for `Char` and even `Bool` - there's a certain order to the elements, and we can enumerate this order.

The type class that defines such enumeration sequences is called `Enum`. It defines two functions: a *successor* `succ`, and a *predecessor* `pred`. Here's its definition:

```haskell
class Enum a where
  succ, pred :: a -> a
  toEnum :: Int -> a
  fromEnum :: a -> Int
  ...
```

The `succ` and `pred` function take a value and produce the next or the previous value of the same type. Each value can be considered assigned a number to it, and the functions `toEnum` and `fromEnum` can transform the number to a value and vice-versa. These functions, therefore, allow making the values of the type `a` *enumerable*:

Here are `succ` and `pred` applied to `Int` and `Char`, respectively:

```
> succ 4
5
> pred 4
3
> pred 'z'
'y'
> succ 'z'
'{'
```

The `toEnum` and `fromEnum` operate as follows:

```
> fromEnum 'z'
122
> toEnum 122 :: Char
'z'
```

Note that the `toEnum` is polymorphic in its return type, therefore the type must be explicitly specified.

We'll cover the `Bounded` type class next. The `Bounded` type class specifies the lower and upper bounds, available for a type.

```haskell
class Bounded a where
  minBound, maxBound :: a
```

Here are a few examples:

```
> minBound :: Int
-9223372036854775808
> maxBound :: Int
9223372036854775807
> minBound :: Char
'\NUL'
> maxBound :: Char
'\1114111'
> minBound :: Bool
False
> maxBound :: Bool
True
```

The only standard type that is a member of `Enum`, but not a member of `Bounded` is the `Integer` type. Trying to get a bound value of an `Integer` will result in an error:

```
> maxBound :: Integer

<interactive>:1:1: error:
    • No instance for (Bounded Integer)
        arising from a use of ‘maxBound’
    • In the expression: maxBound :: Integer
      In an equation for ‘it’: it = maxBound :: Integer
```

#### `Num` and its extensions

The `Num` type class defines operations that can be performed on numeric values. It has a rich hierarchy of extensions, specifying more complex numbers and operations.

```haskell
class Num a where
  (+), (-), (*) :: a -> a -> a
  negate :: a -> a
  abs :: a -> a
  signum :: a -> a
  fromInteger :: Integer -> a

  x - y = x + negate y
  negate x = 0 - x
```

The `Num` type class defines a series of operations that must be implemented. It defines the `+`, `-`, and `*` operations, however, it does not define division `/`. This is due to the fact that division for whole numbers, and numbers with a floating point are implemented differently. The `Num` type class has two extensions: the `Integral` and `Fractional` type classes, the former defines division for whole numbers, the latter - for floating-point numbers.

In reality, the `Integral` type class does not extend `Num` directly, it uses another type class `Real`, which represents all real numbers.

```
> :i Integral
class (Real a, Enum a) => Integral a where
  quot :: a -> a -> a
  rem :: a -> a -> a
  div :: a -> a -> a
  mod :: a -> a -> a
  quotRem :: a -> a -> (a, a)
  divMod :: a -> a -> (a, a)
  toInteger :: a -> Integer
  {-# MINIMAL quotRem, toInteger #-}
  	-- Defined in ‘GHC.Real’
instance Integral Integer -- Defined in ‘GHC.Real’
instance Integral Int -- Defined in ‘GHC.Real’
```

The functions `div` and `mod` are responsible for the division operations, `div` performing integer division, and `mod` finds the remainder. The function `divMod` simultaneously applies `div` and `mod`, returning the result as a pair. The `MINIMAL` pragma suggests that a minimal complete definition requires implementing `quotRem` and `toInteger`.

Haskell contains an implementation of `Integral` for the `Int` and `Integer` types, as shown by the output of the `:i` (`:info`) command.

The other extension for `Num` is the `Fractional` type class:

```
> :i Fractional
class Num a => Fractional a where
  (/) :: a -> a -> a
  recip :: a -> a
  fromRational :: Rational -> a
  {-# MINIMAL fromRational, (recip | (/)) #-}
  	-- Defined in ‘GHC.Real’
instance Fractional Float -- Defined in ‘GHC.Float’
instance Fractional Double -- Defined in ‘GHC.Float’
```

Here we can see that, among others, the `Fractional` type class defines the division operation `/` for floating-point numbers. Haskell includes an instance of this type class for `Float` and `Double`.

The `Floating` type class defines a wide set of operations for floating-point arithmetic:

```
> :i Floating
class Fractional a => Floating a where
  pi :: a
  exp :: a -> a
  log :: a -> a
  sqrt :: a -> a
  (**) :: a -> a -> a
  logBase :: a -> a -> a
  sin :: a -> a
  cos :: a -> a
  ...
  {-# MINIMAL pi, exp, log, sin, cos, asin, acos, atan, sinh, cosh,
              asinh, acosh, atanh #-}
  	-- Defined in ‘GHC.Float’
instance Floating Float -- Defined in ‘GHC.Float’
instance Floating Double -- Defined in ‘GHC.Float’
```

Another extension is the `RealFrac` type class, which defines rounding operations:

```
Prelude> :i RealFrac
class (Real a, Fractional a) => RealFrac a where
  properFraction :: Integral b => a -> (b, a)
  truncate :: Integral b => a -> b
  round :: Integral b => a -> b
  ceiling :: Integral b => a -> b
  floor :: Integral b => a -> b
  {-# MINIMAL properFraction #-}
  	-- Defined in ‘GHC.Real’
instance RealFrac Float -- Defined in ‘GHC.Float’
instance RealFrac Double -- Defined in ‘GHC.Float’
```

There are many more type classes in the `Num` hierarchy. Detailed documentation is available on [Hoogle](https://hackage.haskell.org/package/base-4.12.0.0/docs/Prelude.html#t:Num).

### Non-strict semantics

In imperative languages, instruction order defines the order of execution. In functional languages there are no instructions, so it's not immediately obvious how to define an execution order of arbitrary expressions.

#### Evaluation models

As you may recall, expressions are *reduced*, and their reduction may be performed in any order. Let's look at an example:

```haskell
sumIt :: Int -> Int -> Int
sumIt x y = x + y
```

This simple function sums the two arguments together. Invoking it with the following:

```
> sumIt (1 + 2) 3
6
```

gives us the expected result 6. How can we arrive at this result? There are two possible strategies: the first, used in most programming languages, is called *eager evaluation* (sometimes *strict evaluation*). We first calculate the result of the expression `(1 + 2)`, and only then the function is applied. The second strategy, which is used in Haskell, is called *lazy evaluation*: we first substitute the expressions in the body of the functions, and only then perform the reduction. Here is an example of lazy evaluation reduction steps in Haskell:

```
sumIt (2 + 3) 4
 ~> (2 + 3) 4
 ~> 5 + 4
 ~> 9
```

First, we substitute the expressions in place of the former parameters `x` and `y`, namely `(2 + 3)` and `4`, and inside the body evaluate and reduce the expressions. 

Compared to the eager evaluation:

```
sumIt (2 + 3) 4
 ~> sumIt 5 4
 ~> 5 + 4
 ~> 9
```

Where the expression `(2 + 3)` is evaluated first.

Let's introduce a bit of terminology: an expression that can be simplified further is called a *redex* (short for *reducible expression*).

In the lazy evaluation example above there are two redexes: the first is the expression `(2 + 3)` - the `+` operation can be further simplified. The second redex is the function application itself.

In situations where we have multiple redexes, we can employ different evaluation strategies for them.

In pure functional languages, the same result will always be produced, regardless of the evaluation strategy. This is not guaranteed in imperative languages where order of evaluation matters.

#### Lazy evaluation

Let's look at the properties of lazy evaluation. Consider the following function:

```haskell
add7 :: Int -> Int -> Int
add7 x y = x + 7
```

The number 7 is added to the first argument `x`, the second argument is ignored.

Let's look at the reduction steps for both lazy and eager evaluation strategies:

```
-- lazy
add7 1 (2 + 3)
 ~> 1 + 7
 ~> 8

-- eager
add7 1 (2 + 3)
 ~> add7 1 5
 ~> 1 + 7
 ~> 8
```

In the first case we substitute the formal parameters `x` and `y` of `add7` with the expressions `1` and `(2 + 3)`. Since the function uses only the first argument, the second is completely ignored, therefore the second argument is not evaluated.

In case of the eager evaluations, both expressions are first evaluated, before being bound to the function arguments.

The lazy evaluation strategy is more efficient in this case, since it does not attempt to evaluate expressions that will not be used. However, this is not always the case. Here's an example:

```haskell
dup :: Int -> (Int,Int)
dup x = (x,x)
```

Reducing this using both strategies:

```
-- lazy
dup (2+3)
 ~> (2+3, 2+3)
 ~> (5,2+3)
 ~> (5,5)

-- eager
dup (2+3)
 ~> dup 5
 ~> (5,5)
```

The lazy evaluation strategy requires 4 steps of reduction, while the eager evaluation is more efficient.

Lazy evaluation is preferable when some of the function parameters are ignored, while eager (strict) evaluation is preferable when they are used multiple times in the body of the function.

Luckily, Haskell optimizes for such cases of duplicate use by deferring the evaluation, allowing calculating the result just once. This layer of indirection is called a *thunk*, and it works as follows:

```
dup (2+3)
 ~> (t,t)     -- t = 2+3
 ~> (5,t)     -- t = 5
 ~> (5,5)
```

The thunk `t` points to a value that hasn't yet been calculated. The first time the value is required, it is evaluated, and now the thunk points to the evaluated result, allowing substituting it immediately where it is further required, without reevaluating.

Thunking is what allows lazy languages like Haskell to operate on huge values, such as infinite lists, however, it also slightly complicates our ability to reason about the program, as it turns simple expression trees into graphs.

#### Strict and non-strict semantics

Lazy evaluation has some interesting properties when dealing with programs that do not terminate. In many cases, using lazy evaluation we can eliminate some cases of diverging programs. Let's look at an example:

```haskell
const42 :: a -> Int
const42 = const 42
```

The `const42` function takes one argument and returns an `Int`. It is implemented by calling `const`, passing it the number 42 and the argument. As you recall, the `const` function ignores its second argument, causing our `const42` function to always return the value 42.

```
> const42 True
42
```

Since `const42` always ignores its argument, we can also apply it to a non-terminating computation:

```
> const42 undefined
42
```

The `undefined` function always produces an error, but only when it is evaluated. In our case, the `undefined` function is never used, so it's never evaluated. This makes lazy evaluation suitable for eliminating divergent computations.

Functions, such as `const42` are called *non-strict*. Formally, a non-strict function is a function that accepts a non-terminating (diverging) computation as an argument, but still produces a result (converging), it is considered non-strict. Conversely, a *strict* function, given a diverging computation as an argument, becomes divergent itself.

This allows us to separate functions into two kinds: strict and non-strict. However, in some functions, the strictness of a second argument may depend on the first. This makes *strictness analysis* into a non-trivial problem. The Haskell compiler performs strictness analysis to reduce the cost of lazy evaluation, which sometimes can lead to better performing and more effective programs.

#### Weak Head Normal Form

In functional languages, expressions are reduced until they cannot be reduced further. The reduction process happens for as long as there are *redexes* that remain in the expression, resulting in an expression that no longer contains any redexes. Those fully-reduced expressions are in a so-called *normal form*, meaning that no more reductions are possible.

In Haskell, there exists an intermediate reduction stage, called *weak head normal form* (abbreviated WHNF). Let's look at some examples:

```
-- Normal Form
42
(3,4)
\x -> x + 2
```

The three expressions above are all in a normal form (NF). The first is a number 42, which has no other reduction steps. The second is a pair constructor, which is applied to the values 3 and 4, written in a *mixfix* style. This is also a value which cannot be reduced. The third example is a lambda expression. It too cannot be further reduced, since it does not contain any redexes (the `+` operator is considered *built-in*, and it cannot be applied until both arguments are available).

Now let's look at expressions which are not in NF:

```
-- not NF
"Hello " ++ "world"
sin (pi / 2)
(\x -> x + 2) 5
(3,1+5)
```

Redexes exist in all of the above examples, meaning they can be further reduced, therefore are not considered normal form.

Weak head normal form is a special case of an expression which contain redexes, consisting of the following:

1. a lambda *abstraction*
2. a data constructor
3. any built-in partially-applied operator

Here are some examples of WHNF:

```
-- WHNF
\x -> x + 2*3
(3,1+5)
(,) (4*5)
(+) (7^2)
```

The first example is a lambda abstraction. It's not in NF since it contains a redex `2*3`, however when this expression is inside the lambda body, it is considered WHNF. The second example is a data constructor (tuple, in this case), which contains a reducible expression `1+5`. However, because it occurs inside a data constructor, this is also considered WHNF. The third and fourth examples are built-in Haskell operators, partially-applied to a redex. This is also considered a WHNF.

It is said that expressions in NF are also at the same time WHNF. In most cases, Haskell will stop reducing expressions at WHNF, not reducing it further to NF. This allows Haskell to optimize functions for strictness.

#### Forcing strictness

We now know the meaning of lazy evaluation semantics. If an expression is not required - it will not be evaluated. In most cases this is a desired property, however, there are some cases this causes problems.

Haskell uses deferred execution, or, thunking, to perform lazy computations. In working with large data structures, such as lists of an arbitrary length, thunks may accumulate in memory. Suppose we're summing a list of 10 million elements; in the lazy evaluation model, a thunk will have accumulated 10 million deferred `+` operations, ready for evaluation, but it cannot happen until all elements have been processed.

Memory, or more specifically, *space leaks* is a common problem in Haskell, and often requires careful solutions. Sometimes, we'd like to instruct the Haskell compiler not to defer any computations, but perform them as soon as they're available. This is achieved by using the Haskell primitive `seq`.

The `seq` primitive is a function that is used to force strict evaluation for a given computation. Let's see how this function could be defined (in pseudo-code), and its uses:

```haskell
seq :: a -> b -> b
seq ⊥ b = ⊥
seq a b = b
```

The `seq` function can be though of as a function of two arguments, returning the second argument and ignoring the first. If it only had one definition (line 3 of the example above), it would be the same as using `flip const`. Such a definition is only possible in a lazy language, since it requires deferring the evaluation of the arguments. However, the definition above is not a valid Haskell syntax, as we're using a concept called *bottom* (also called *falsum*, denoted by the Unicode symbol ⊥ or an ASCII sequence `_|_`), which signifies non-terminating, or, divergent computations. If the first argument to `seq` is diverging, the result will also be diverging.

This function cannot be directly implemented using Haskell syntax, however it's a built-in Haskell primitive.

Let's see a few examples of using `seq`:

```
> seq 1 2
2
> seq undefined 2
*** Exception: Prelude.undefined
> seq (id undefined) 2
*** Exception: Prelude.undefined
```

Instead of ignoring its first argument, Haskell attempts to reduce it until WHNF. If this attempt fails (if the computation is divergent), `seq` fails as well.

Let's see some examples where using WHNF with `seq` does not diverge:

```
> seq (undefined,undefined) 2
2
> seq (\x -> undefined) 2
```

Because both expressions above are already WHNF, `seq` is satisfied and does not attempt to reduce it further, returning the second argument.

#### Strict function application (call-by-value)

Even though the `seq` primitive is useful, it's not very convenient. Haskell defines a more convenient *call-by-value* operator `$!`, which can be used instead of `seq`:

```haskell
($!) :: (a -> b) -> a -> b
f $! x = x `seq` f x
```

The type of the `$!` operator is identical to the `$` operator, taking a function `a -> b` and an argument `a`, producing a `b`. Here, it is using `seq` in the infix style, and means the following: the argument `x` is first reduced until WHNF, and then the function `f` is applied to the reduced `x`. Reduction here happens before function application, allowing the operator to force strictness. Let's see some uses of this operator:

```
> const 42 undefined
42
> const 42 $ undefined
42
> const 42 $! undefined
*** Exception: Prelude.undefined
```

In the example above, we can see that the `$!` operator works similarly to `$` (they have the same precedence and associativity), however, the `$!` forces the evaluation of its arguments. Since `undefined` diverges, the result of `$!` diverges as well.

Let's see a real example where this is useful. Consider our `factorial` function:

```haskell
factorial :: Integer -> Integer
factorial n | n > 0     = helper 1 n
            | otherwise = error "arg must be >= 0"
  where
    helper acc 0 = acc
    helper acc n = helper (acc * n) (n - 1)
```

The `helper` function will recursively call `helper` until `n` reaches 0, accumulating nested calls to `helper` with decreasing `n` values. In reality, Haskell's strictness analysis can handle this situation, and turn them into strict calls, however if we want to make sure this optimization happens, we could use the `$!` operator to force this strictness ourselves:

```haskell
  ...
  helper acc n = (helper $! (acc * n)) (n - 1)
```

This change forces Haskell to evaluate the first argument to `helper`, allowing us to eliminate the chain of nested computations. In addition, since the `$!` operator has a low precedence, we must enclose the expression in parentheses.

### Modules and compilation

Haskell programs are a collection of *modules*. The main module is called `Main`, and each module should reside in a file named after the module, although that's not required. Inside the file, a module is declared by the keyword `module`, followed by the module name (starting with a capital letter), followed by the `where` keyword.

#### Modules

In the file `Demo.hs`, we have the following definition:

```haskell
module Demo where
```

We can now add our own definitions and imports. The `Prelude` module, which contains many basic functions is implicitly imported in our `Demo` module, and we can start using its functions in our module immediately.

To use a function defined in another module, that module must first be imported by using the `import` keyword:

```haskell
module Demo where

import Data.Char
```

The `import Data.Char` directive imports all functions that are exposed in the module. Sometimes we don't need all the functions, so we can specify in parentheses the names of the functions we wish to import:

```haskell
import Data.Char (toUpper,toLower)
```

Sometimes we need the opposite operation - import all functions *except* the specified ones. This is allowed by using the keyword `hiding`:

```haskell
import Data.Char hiding (toLower)
```

Suppose we want to import the function `union` from `Data.List`. Another `union` function is also defined in `Data.Set`. Importing both modules, then trying to use the `union` function will result in the following error:

```haskell
import Data.List
import Data.Set
```

```
> :t `union`

<interactive>:1:1: error:
    Ambiguous occurrence ‘union’
    It could refer to either ‘Data.Set.union’,
                             imported from ‘Data.Set’
                             (and originally defined in ‘Data.Set.Internal’)
                          or ‘Data.List.union’,
                             imported from ‘Data.List’
                             (and originally defined in ‘base-4.12.0.0:Data.OldList’)
```

The error suggests an ambiguity - Haskell is unable to determine which one of the `union`s we meant. Instead, we can use the fully-qualified name, e.g. `Data.List.union`:

```
> :t Data.List.union
Data.List.union :: Eq a => [a] -> [a] -> [a]
```

However this is not often convenient. In some cases we'd like to always refer to a function by its fully-qualified name. For this, there exists a keyword `qualified` which imports module members with a fully-qualified name:

```haskell
import Data.List
import qualified Data.Set
```

Here, the ambiguity no longer occurs, since the `union` function from the `Data.Set` module must always be used fully-qualified:

```
> :t union
union :: Eq a => [a] -> [a] -> [a]
```

Because the module names are hierarchical, the sometimes can be very long, and using the fully-qualified name proves cumbersome. Haskell allows to alias module names, allowing to locally rename them to something shorter, by using the `as` keyword:

```haskell
import qualified Data.Set as Set
```

Allowing accessing it by the shorter name:

```
> :t Set.union
Set.union  :: Ord a => Set.Set a -> Set.Set a -> Set.Set a
```

In rare occasions we'd like to implement a function that already exists in the `Prelude`. In this case, the `Prelude` module must be explicitly imported, hiding the functions that we wish to override locally. All explicitly-imported modules override any implicit ones.

#### Exporting modules

Importing modules allows us to use functions declared in other modules. There is an opposite directive - `export`, which controls which functions from our module are visible to others.

Let's create two modules in two separate files, `Demo.hs` and `Test.hs`. In the `Test` module we declare the following functions:

```haskell
module Test where

sumIt x y = x + y

const42 = const 42
```

In the `Demo` module:

```haskell
module Demo where

import Test

f1 = const42 True

f2 = sumIt 3 4
```

Let's load it in GHCi:

```
 $ ghci
GHCi, version 8.6.5: http://www.haskell.org/ghc/  :? for help
Prelude> :l Demo
[1 of 2] Compiling Test             ( Test.hs, interpreted )
[2 of 2] Compiling Demo             ( Demo.hs, interpreted )
Ok, two modules loaded.
```

The Haskell compiler first attempts to compile and load the imports, and then the actual module we've requested. If everything loaded without errors, we'll see the "Ok, two modules loaded" message.

If we want to limit the functions that are available to other modules, we can *export* just some of them, by specifying their names in parentheses after the module name. In our `Test` module, let's only export the `sumIt` function:

```haskell
module Test (sumIt) where
```

Saving, then reloading our GHCi session will produce the following error:

```
*Demo> :r
[1 of 2] Compiling Test             ( Test.hs, interpreted )
[2 of 2] Compiling Demo             ( Demo.hs, interpreted ) [Test changed]

Demo.hs:5:6: error:
    • Variable not in scope: const42 :: Bool -> t
    • Perhaps you meant ‘const’ (imported from Prelude)
  |
5 | f1 = const42 True
  |      ^^^^^^^
Failed, one module loaded.
```

The interpreter reports that the compilation failed, only the `Test` module was loaded. The `Demo` module reports an error that the `const42` function is not available.

The export directive is Haskell's only mechanism for encapsulation. Similarly to object-oriented languages, where encapsulation is a means of hiding implementation details from public API, in Haskell, exporting only certain functions is the only way to keep some of the functions *private* to the module.