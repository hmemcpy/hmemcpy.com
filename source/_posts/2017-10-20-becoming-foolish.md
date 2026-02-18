---
title: "Becoming Foolish"
date: 2017-10-20 08:00:39
tags:
---
The book [*The Pragmatic Programmer: From Journeyman to Master*](https://pragprog.com/book/tpp/the-pragmatic-programmer) by Andy Hunt and Dave Thomas suggests that as developers, we should "learn at least one new language every year." (pg. 14)

When I recently asked a roomful of developers, if there's anyone who had learned a new language this year, only very few hands went up. A year ago today, that would have been me in the audience, keeping my hands down.

<!-- more -->

I had been a happy C# developer for over a decade, starting professionally sometime before .NET 2.0 was released. During my career I had the privilege of working in a very specialized field - building tools for other developers, mainly in form of extensions to Visual Studio itself. My job often required me to understand the code better than the compiler, in fact, I often had to take a peek under the hood to understand what the compiler, MSIL, JIT, and sometimes native code were doing, all long before tools like [Roslyn](https://github.com/dotnet/roslyn) even existed. I knew implementation details of the runtime that were not documented anywhere. I knew most of the corner cases and language gotchas. But overall, my language, C#, was a very powerful hammer, capable of handling any kind of nail.

Which caused me to pretty much ignore any other languages out there, which weren't relevant to my day job. Whenever people from the F# camp were boasting their lack of nulls, pattern matching, or not needing semicolons or braces, I would typically shrug it away. I have spent years of my career learning to use productivity tools, such as ReSharper and IntelliJ IDEA, to the point where every bit of boilerplate was one keystroke away. I simply didn't care! Having a few nice features was never a good enough reason for me to switch a programming language -- why would I even bother, when my language that I'm an expert in, could kinda-sorta do that too? Why would a different *syntax* make a difference in how I write software? After all, doesn't it all compile down to the same thing?

Because when you really get down to it, (almost) all programming languages are, essentially, this:

```java
public static void main(String[] args)
{
    ...
}
```
In most programming languages that we've ever experienced, the world as we know it *lives and dies* in the confines of the opening and closing brace of the `main` function, which is the entry point to our application. Everything that happens in our program, the universe our program interacts with, happens between those two braces. By its very definition, our program returns an *exit code*, specifying whether it succeeded or not, and everything else happens as a side-effect.

The implication, that all the work is done between the two braces of the `main` method, is what drives **everything** we know about this model --- every design pattern, every practice, every discipline, every tool, library, or framework --- were created to let us manage this model of our world that exists between those two braces. We have decades of knowledge in how to do this properly in almost any language.

For me, this was the core, the very foundation on which all the software is built! It was the one thing that was the ultimate truth, regardless of the programming language.

And it was like this, until **Haskell ruined it for me**!

I will not go into details -- I inadvertently did that in my [previous post](/2017/05/from-net-to-scala-and-beyond-a-journey-to-functional-programming/). But during watching a talk on seemingly unrelated topic, the speaker managed to sneak some Haskell in there! Until that moment, I haven't really seen any Haskell code before --- I've always dismissed it as irrelevant --- and there it was,  staring me in the face.

```haskell
main :: IO () -- reads as 'main, having the return type of IO ()'
```

What I saw being explained is that Haskell doesn't actually do any work inside of its `main` function. Instead, the program "describes" in a declarative way what is going to have happen when your program executes, and this "description" will be returned into the Haskell runtime, and exactly what was described will happen - with no possible *side-effects* or surprises. It flips the entire idea of execution on its head - the work, the actual execution of effects is not being done *inside* of `main` - it's done on the *outside*!

Seeing this for the first time, trying to wrap my head around it, had created a *bug* inside my head. It had conflicted with what I knew - that all languages worked the same, and the difference was merely syntax! But here, I was seeing something that just worked differently, and did not fit my world view! I struggled with trying to understand it, and it took me a couple of more re-watches, until one day, it finally clicked!

In one single moment, I suddenly understood the *idea* of Haskell, of why it works the way it does. Everything just clicked into place and I finally "understood monads"! To me, it felt like Neo finally coming to terms with the fact that [there is no spoon](https://www.youtube.com/watch?v=uAXtO5dMqEI), and only then he's able to bend it. 

I am thankful for [Andrea Magnorsky](https://twitter.com/silverSpoon)'s excellent keynote talk, [Inviting Everyone to the Party](https://www.youtube.com/watch?v=WBu43Tj0zOY), which helped me realize that not only what I had experienced had a name, it was, in fact, a textbook definition of the phenomenon: what I had experienced is called a **paradigm shift**.

The term "paradigm shift", coined by [Thomas Kuhn](https://en.wikipedia.org/wiki/Thomas_Kuhn) in his 1962 book [The Structure of Scientific Revolutions](https://en.wikipedia.org/wiki/The_Structure_of_Scientific_Revolutions), describes a process where if an established model no longer fits the world view, it is rejected and simultaneously replaced by another. Kuhn says:
{% blockquote Thomas Kuhn, The Structure of Scientific Revolutions: 50th Anniversary Edition (pg. 78) %}
The decision to reject one paradigm is always simultaneously the decision to accept another, and the judgment leading to that decision involves the comparison of both paradigms with nature and with each other.
{% endblockquote %}

I had two conflicting ideas, and when finally that other idea started making sense, my mind accepted it, and immediately switched to that new idea - the switch was instantaneous! I was able to see things from a different perspective, understanding a whole new world model, which is precisely the definition of Kuhn's "paradigm shift".

But something else happened -- I realized just how little I knew about software, there was an entire world out there that was unknown to me! What I knew until that moment, all my expertise in a narrow field was just a tip of the iceberg. And this realization removed a barrier I had that prevented me from trying to learn new languages and experimenting with new things. Where previously I would dismiss these things as irrelevant, I suddenly gained interest in things that I never had interest in before. In the past year alone I've used Haskell, Clojure, and Rust. I've looked at Erlang, Elm and PureScript. I am working my way through [SICP](https://mitpress.mit.edu/sicp/full-text/book/book.html) (see [modern PDF compilation](https://github.com/sarabander/sicp-pdf)) and learning [Category Theory](https://github.com/hmemcpy/milewski-ctfp-pdf). I've done all that because for the first time in a long time, I am genuinely curious about what these languages/paradigms can *teach* me! I really don't remember the last time I was this excited about learning. Genuinely proud of being able to say -- "I don't know everything!" -- is incredibly liberating!

This exact sentiment is also echoed in Bret Victor's fantastic, and highly entertaining keynote talk, [The Future of Programming](https://vimeo.com/71278954), where he pretended he was a software developer in 1973, and speculated about the next 40 years of programming. The last 5 minutes of that talk has some of the best advice I ever heard, and I wish I understood it sooner. He said,
{% blockquote Bret Victor https://vimeo.com/71278954 The Future of Programming %}
...you have to say to yourself -- "I don't know what I'm doing. We, as a field, don't know what we're doing. We don't know what programming is, we don't know what computing is, we don't even know what a computer is." And once you truly understand that, once you truly believe that -- then you're free, and you can think anything.
{% endblockquote %}

*Stay hungry. Stay foolish.* Be free!
