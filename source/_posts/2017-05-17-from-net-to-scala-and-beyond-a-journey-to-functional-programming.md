---
title: "From .NET to Scala and beyond: a journey to Functional Programming" 
date: 2017-05-17 11:24:13
tags:
---
*Original title was "Monads solve a problem you might not have, but it's a nice problem to have", which is an homage to a [great post](http://kozmic.net/2012/10/23/ioc-container-solves-a-problem-you-might-not-have-but-its-a-nice-problem-to-have/) by [Krzysztof Koźmic](https://twitter.com/kkozmic) about IoC containers.*

I can't think of another 5-letter word that strikes fear in the hearts of so many developers, coming from an object-oriended/imperative language to a functional one. So much so, this, and other M-words are outright [banned](https://fsharpforfunandprofit.com/about/#banned) on some resources.

This post will not attempt to explain monads, at least, not on purpose. This [fantastic post](https://mkremins.github.io/blog/doors-headaches-intellectual-need/) by [Max Kreminski](https://twitter.com/maxkreminski) does this better than I ever could - by showing that most "monad tutorials" (or, educational blog posts in general) have *problem-solution ordering issues*. Please take a moment to read this wonderful post before continuing.

<!-- more -->

The problem with most monad tutorials is they present monads as a solution to a problem which is not clearly defined.

Recently, I had my own epiphany, and finally "understood monads". That is, I've re-watched the same talks on the subject so many times, until it finally clicked. But then, something magical happened: just as Douglas Crockford [predicted](http://lambda-the-ultimate.org/node/4670), I lost my ability to explain it to others. And yet, I gained a retroactive understanding of the, previously literally-Greek, definitions. I developed an intuition that helped me understand the reasons and logic behind those definitions.

With great power comes great responsibility of NOT writing yet another tutorial. Instead, I will use these powers for good, trying to recreate the *intellectual need* (as Max' post puts it) for a problem that has monads as a solution.

## Unlearning to walk

The hardest part in learning something so radically different, is trying to apply it what you know already, failing miserably.

About a year ago (at the time of writing), I decided to take a break from .NET, and go explore what else was out there. I landed a job at Wix.com, which I knew to be a (mostly) Scala company on the backend. As first step, I needed to learn Scala. There are plenty of great resources around, but pretty quickly it became apparent that there are two camps of Scala: those who use it as a "better Java" - a language with short, concise syntax, which has great support for many functional concepts, and those who use it as a kind of Haskell on the JVM.

For most people coming from imperative/object-oriented languages, mere mention of Haskell typically results in pushing the back button in their browser. Haskell is usually associated with academics and recent university graduates, who had taken a course on FP. Until very recently, I was proudly in the group who dismissed Haskell as something irrelevant to me, because I could not imagine it being useful for solving Real Life&trade; problems, like building a Visual Studio plugin, or even typical CRUD app.

Little did I know that a simple Hello World app in Haskell would change my views forever.

### Functional inception

I was watching a talk by [Rúnar Bjarnason](https://twitter.com/runarorama), one of the authors of the book [Functional Programming in Scala](https://www.manning.com/books/functional-programming-in-scala) (AKA the "Red Book"), titled [Purely Functional I/O](https://www.infoq.com/presentations/io-functional-side-effects), which I highly recommend watching (at least, the first half, if you are not using Scala). He outlines the principles of functional programming, and why we can't really do "pure" FP in most programming languages. The problem lies with the fact that any function can perform I/O, or "have side-effects", causing us to lose most of the benefits of functional programming. 

The benefits, outlined in [this post](http://degoes.net/articles/easy-monads) by John A De Goes, are just 3 properties that functions must exhibit:

1. **Totality**. A function must yield a value for every possible input.
2. **Determinism**. A function must yield the same value for the same input.
3. **Purity**. A function’s only effect must be the computation of its return value, *and nothing else*.

These properties are voilated by "side-effects". We consider side-effects to be anything like reading a file, talking to a web server, starting threads, throwing exceptions, etc. To be precise, functions that have side-effects violate [referential transparency](https://en.wikipedia.org/wiki/Referential_transparency) (RT), a fundamental property of functional languages, where expressions that make up a program can be safely replaced with the result of evaluating said expression, without changing the program's behavior. A function is considered "pure", if it is RT for all RT arguments, meaning that the arguments passed into a function must be pure themselves. A side-effect, therefore, is *anything* that violates RT.

In this world of pure functions that always return a value, there is no such thing as `void`. All functions must return a value, and that value must always be the same for the same input. Given these "restrictions", how can we possibly do anything useful (e.g. talking to a database) in a functional language?

### Hello, (functional) World

Here's when my worldview flipped on its head. In practically any programming language in the world you can write a program that says hello. It will typically look like this in C#:

```csharp
Console.WriteLine("What is your name?");
Console.WriteLine("Hello " + Console.ReadLine());
```

or like this in Scala:

```scala
printLn("What is your name?")
printLn("Hello " + readLine)
```

When this program is compiled and run, it will print the first line to the screen, then wait until we type something and press enter. It will concatenate our input with the string `"Hello "`, printing the combined string to the screen. This is universally true in almost any programming language out there.

If we try to write the same program in Haskell:

```haskell
putStrLn "What is your name?"
putStrLn ("Hello, " ++ getLine)
```
It will not even compile, giving us the following error:

> Couldn't match expected type `String` with actual type `IO String`  
> In the second argument of `(++)`, namely `getLine`

The error tells us that the value returned from the `getLine` function is not a `String`, but rather something called `IO String`. What IO is doesn't matter right now, but the point is, they are incompatible types. The IO serves as a wrapper, a container over some string value.

The most obvious and immediate question is -- fine, I have an `IO String`, how do I get the `String` out? The answer is - you *can't*. There is no way to get the string out of `IO` using normal means. The only way to use the value is to **bind** it to another function (using a funny-looking Haskell operator `>>=`, pronounced `bind`). Here is what the "fixed" program looks like:

```haskell
main :: IO ()
main = putStrLn "What is your name?" >> 
       getLine >>= \n -> putStrLn ("Hello, " ++ n)
```

Which *binds* the result of `getLine` with the input parameter `n` of a Lambda expression (Lambdas in Haskell are defined with a `\`, which makes it look like the symbol `λ`), which passes it to the `putStrLn` function.

Another way of writing this program is with a **do-notation**, which makes it look more imperative:

```haskell
main :: IO () 
main = do 
  putStrLn "What is your name?" 
  name <- getLine 
  putStrLn ("Hello, " ++ name)
```

The `name <- getLine` expression would be the equivalent of `from name in getLine` expression in a LINQ query.

### Enter the Monad

It should be no surprise at this point to discover that `IO` is a **monad**, [everything in Haskell is a monad](https://twitter.com/nixcraft/status/739383796626128896). I haven't yet attempted to explain what a monad is, and for now, I'm not going to. Instead, I'd like to try and explain the purpose of this construct, and why it is used.

Haskell is a **purely-functional**, lazily-evaluated language. By definition, it has a limitation - all of its functions must be pure. This may sound very limiting - we can't just do a `File.Open` in the middle of a Haskell function - it just won't work. However, this gives us a very interesting benefit: since all functions in Haskell are pure, therefore referentially transparent, this means every Haskell program is a *single referentially transparent* expression! A program in Haskell represents an exact *description* of what it is about to do - it's pure data, as far as the developer (and Haskell compiler) is concerned. Reading a Haskell program describes **exactly** what is going to happen, when this program executes. There are no surprises, no *side-effects* to this.

Which brings me to the `IO` type. In Haskell, it is used to represent a value that is dependent on some I/O operation. We don't know (we can't know) what the value is - but it isn't important. The *effect* that the `IO` type has is to produce a value that depends on an interaction with the outside world, but as far as the Haskell compiler is concerned - the "value" of this type is just that - *some value* of type `IO String`. This gives semantic meaning to the underlying value, puts it in a context of being dependent on an I/O operation.

In Haskell, and languages like Scala, F# and others we have an `Option` type (called `Maybe` in Haskell), whose purpose is to represent a value which may or may not be there. Regardless of whether or not the value exists, we can still perform operations on the `Option` type: we can pass it around, we can transform and `bind`/`map` its value with others. The *effect* of the `Option` type is to represent an optional value.

Both `IO` and `Option` fulfil a purpose of representing an underlying value (or values) in a certain context. For `IO`, this context is an interaction with the outside world. For `Option`, the context is optionality. Both these types are **monads**. Their purpose is to explicitly encode the type of **effect** performed by those types within the type definition itself. In essense, monads are used explicitly to represent the context in which the underlying values are computed, without actually having to directly interact with those values.

### Learning to walk again

Which finally bings me to the point of this apparent "intro to Haskell" tutorial I ended up writing: it turned out that turning implicit side-effects into explicit monadic context was extremely useful for other concerns as well, such as reading values from some environment (the Reader monad, functional equivalent of "dependency injection"), writing to a log file (the Writer monad), modifying state (the State monad), and others. Problems that, superficially, seem different, could be solved using a very similar pattern. Unfortunately, as Max Kreminski put it in his [post](https://mkremins.github.io/blog/doors-headaches-intellectual-need/), it takes a lot of writing code in a functional language to begin seeing this pattern.

In Haskell, monads helped solve the problem of controlling effects, because there's just no other way, therefore they are first-class concepts built into the standard library. In other (strict) functional languages like F# or Scala, they are optional, and can be used together with "impure" code.

Most importantly, monads are just another tool in the toolbox. They are useful, but not the most important thing in FP.

## Conclusion

When I began writing this post I had no idea where it would go. I promised I won't try to explain monads, but I feel that I inadvertently have. I would like to conclude with the following:

I'm sorry, dear C# developers, no amount of tutorials are going to help you understand monads. Eric Lippert [made a great attempt](https://ericlippert.com/category/monads/) once, a whopping 13-part series, explaining monads in C#. Unfortunately, Eric suffers the same "monads tutorial" fallacy, losing many people around post #2. The series of posts is still highly recommended, however, as a great history behind LINQ, which is the closest thing to monadic computations C# currently has.

The reason? Most problems in C# (or Java, or Ruby, or any other imperative language) are just solved differently - existing [monad solutions](https://github.com/louthy/csharp-monad) feel needlessly complicated where a simple `if` statement or a `null` check will suffice. You end up fighting the type system, needlessly verbose annotations and awkward syntax, just trying to use a "monadic" solution (not to mention the runtime overhead of needlessly creating closures).

Unfortunately for you, the only way forward is realization that what we know as OOP had lived to its maximum potential. There's nothing wrong with OOP per-se, but if you feel you've had [Enough!](http://hmemcpy.com/2017/03/enough/) with ever-growing complexity, fighting tests or IoC containers, or general feeling of solving the same issues over and over, year after year, perhaps it's time to consider moving onto something completely different.

And that's what Functional Programming is to OOP - just different. The goal is the same - working software, the means of getting there is just different. For better, or worse.
