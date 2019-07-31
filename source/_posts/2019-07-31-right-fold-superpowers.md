---
title: Right fold superpowers!
date: 2019-07-31 09:25:58
tags:
---
It's amazing how sometimes just having a different framing of the problem helps with developing a much deeper understanding of the problem. I was working through the exercises of the [Data61 Functional Programming course](https://github.com/data61/fp-course), assisted by Brian McKenna's [video streams](https://www.youtube.com/watch?v=NzIZzvbplSM&list=PLly9WMAVMrayYo2c-1E_rIRwBXG_FbLBW), and I came accross a definition of a *right fold* that can be thought of as "constructor replacement":

{% blockquote Tony Morris https://vimeo.com/64673035 Explain List Folds to Yourself %}
The expression `foldr f z list` replaces in `list`:
 1. Every occurence of the cons constructor `(:)` with `f`
 2. Any occurrence of the nil constructor `[]` with `z`
{% endblockquote %}

<!-- more -->

<br/>Or, to put it in a tweet:
<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Intuition for `foldr` as &quot;constructor replacement&quot; is very helpful! <br><br>Given a list:<br><br>1 : 2 : 3 : []<br><br>foldr &quot;replaces&quot; the cons constructor (:) with a function:<br><br>1 `f` 2 `f` 3 `f` []<br><br>e.g.<br>foldr (*) 1 (1 : 2 : 3 : [])<br>replaces : with *, and [] with 1<br>== 1 * 2 * 3 * 1<br>== 6</p>&mdash; Igal Tabachnik (@hmemcpy) <a href="https://twitter.com/hmemcpy/status/1156061465532653568?ref_src=twsrc%5Etfw">July 30, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

So let's use this new intuition to solve some course exercises using right folds only!

**Note**: you should attempt solving them yourself first! Spoilers ahead!

Let's start with [**List.hs**](https://github.com/data61/fp-course/blob/master/src/Course/List.hs):

We get a definition of a list as follows:
```haskell
data List t = Nil | t :. List t
```
Like the builtin Haskell list type `[]`, this custom `List` is comprised of nil and cons data constructors, `Nil` and `:.`. The List module also defines a `foldRight` function that operates on this `List`. We will use all this information to implement the functions for `List` using `foldRight` only.

Let's start with a couple of easy ones: `product` and `sum`. Given the following list:

```haskell
1 :. 2 :. 3 :. Nil
```

to get the product of all values, we replace:
 1. `:.` with `(*)`
 2. `Nil` with the neutral value `1`.
 
Using `foldRight`, we can now implement the `product` function like so:

```haskell
product :: List Int -> Int
product xs = foldRight (*) 1 xs
```

Thanks to [Eta reduction](https://sookocheff.com/post/fp/eta-conversion/), we can drop `xs` from both sides of the equals sign, leaving us with:

```haskell
product :: List Int -> Int
product = foldRight (*) 1
```

The `sum` function is implemented similarly, replacing `:.` with `(+)` and `Nil` with `0`:

```haskell
sum :: List Int -> Int
sum = foldRight (+) 0
```

Let's look at some more interesting functions in the List module.

## headOr
The `headOr` function has the following signature:
```haskell
-- | Returns the head of the list or the given default.
--
-- >>> headOr 3 (1 :. 2 :. Nil)
-- 1
--
-- >>> headOr 3 Nil
-- 3
headOr :: a -> List a -> a
headOr n list = foldRight _cons _nil list
```
The `_cons` and `_nil` arguments are placeholders, also called "typed holes". This is a great Haskell feature, forcing the compiler to provide enough information about what types and values "fit" into those holes. We'll use this information a bit later.

Let's start from the end: the last argument to `foldRight` is our list. Since it appears on both sides of the equation, we can omit it, simplifying to:
```haskell
headOr :: a -> List a -> a
headOr n = foldRight _cons _nil
```
Next is the replacements of the cons constructor `:.` and `Nil`. Let's write down what we want our list to look like, using examples in the function signatures as guides. Here's what our list looks after being "replaced" by `foldRight`:
```haskell
1 `f` 2 `f` 3 `f` n
```
Where `Nil` was replaced by the value `n`. What should the function `f` be? 

The `foldRight` function expects the `f` to be a function with two arguments. In our case, we want to take just the first argument, ignoring everything else.

If we write down our list in a prefix notation, it becomes a bit more apparent:
```haskell
f 1 (f 2 (f 3 n))
  ^ ^^^^^^^^^^^^^
  | |
  | +---- second argument
  +------ first argument
```
To satisfy the requirement of a binary function that ignores its second argument, we can write a lambda function `\a _ -> a`, which takes two arguments and returns the first one:
```haskell
headOr :: a -> List a -> a
headOr n = foldRight (\a _ -> a) n
```
To go one step further, there exists a function called `const`, which ignores its second argument, returning the first. This allows us to replace the lambda with `const` and simplify the call even further, dropping the `n` thanks to Eta reduction:
```haskell
headOr :: a -> List a -> a
headOr = foldRight const
```
## length
Following the steps above, the `length` function:
```haskell
-- | Return the length of the list.
--
-- >>> length (1 :. 2 :. 3 :. Nil)
-- 3
length :: List a -> Int
```
Similarly to `headOr`, we want replace the `:.` constructor with a function. Looking again at our list in its prefix form:
```haskell
f 1 (f 2 (f 3 n))
```
In this case, we want to add `+1` for every `f` that we encounter, completely igoring the first argument. We can do this with a lambda that looks like this: `\_ b -> 1 + b`, which we can further simplify to `\_ -> (1 +)`, dropping the `b` on both sides. Finally, we replace `Nil` with `0`, and our result is:
```haskell
length :: List a -> Int
length = foldRight (\_ -> (1 +)) 0
```
## map
```haskell
-- | Map the given function on each element of the list.
--
-- >>> map (+10) (1 :. 2 :. 3 :. Nil)
-- [11,12,13]
map :: (a -> b) -> List a -> List b
map f = foldRight _cons _nil
```
With `map` we want to preserve the data constructors, applying the mapping function `f` to every element of the list. The typed hole suggests our first argument to `foldRight` needs to have the type `a -> List b -> List b`. We can satisfy it with the function `\a bs -> f a :. bs`. The `Nil` remains unchanged, and our final result is:
```haskell
map :: (a -> b) -> List a -> List b
map f = foldRight (\a bs -> f a :. bs) Nil
```
## filter
```haskell
-- | Return elements satisfying the given predicate.
--
-- >>> filter even (1 :. 2 :. 3 :. 4 :. 5 :. Nil)
-- [2,4]
filter :: (a -> Bool) -> List a -> List a
filter p = foldRight _cons _nil
```
Very similar to `map`, except we use the predicate `p` to decide whether to take the element or drop it from our resulting list. The typed hole for `_cons` is `a -> List a -> List a`, satisfied with:
```haskell
\x xs -> if p x then x :. xs else xs
```
(I'm not using the names `a` and `as` because it screws up the syntax highlighter)

If the element `x` matches the predicate `p`, cons it to our result, otherwise just return the result. Final version:
```haskell
filter :: (a -> Bool) -> List a -> List a
filter f = foldRight (\x xs -> if f x then x :. xs else xs) Nil
```
## (++) aka append
```haskell
-- | Append two lists to a new list.
--
-- >>> (1 :. 2 :. 3 :. Nil) ++ (4 :. 5 :. 6 :. Nil)
-- [1,2,3,4,5,6]
(++) :: List a -> List a -> List a
```
Here is where it gets mindblowing. The `(++)` function takes two lists and appends them. Let's visualize the two lists like this:
```haskell
1 :. 2 :. 3 :. Nil
                4 :. 5 :. 6 :. Nil
```
This makes it very easy to see how we can use "constructor replacement" to append two lists: the `:.` remains unchanged, and we replace `Nil` with the second list! The result is:
```haskell
(++) :: List a -> List a -> List a
(++) list1 list2 = foldRight (:.) list2 list1
```
## flatten
```haskell
-- | Flatten a list of lists to a list.
--
-- >>> flatten ((1 :. 2 :. 3 :. Nil) :. (4 :. 5 :. 6 :. Nil) :. (7 :. 8 :. 9 :. Nil) :. Nil)
-- [1,2,3,4,5,6,7,8,9]
flatten :: List (List a) -> List a 
```
Here is again the intuition for constructor replacement helps us find the answer - the `flatten` functions takes a list of lists and *appends* them together into a single list! This should sound very familiar, as we *just* implemented a function that does that! We can use the `(++)` function to append two lists together, so all we need to do is replace the `:.` between the lists with `(++)`! The result is:
```haskell
flatten :: List (List a) -> List a 
flatten = foldRight (++) Nil
```
---
Hopefully, by now, it became clear how thinking of the right fold as "constructor replacement" can help visualize and guide towards the correct implementation. I recommend finishing the rest of the `List` module, then implement the `Optional` module using only `foldRight`.

I will continue the [Data61 FP course](https://github.com/data61/fp-course), and will share more gems as I learn them! Stay tuned!
