---
title: JetBrains + Nemerle = Limitless Potential!
date: 2012-06-23T17:17:00+00:00
---
There has been some excitement last Friday, as JetBrains' .NET tools program manager Ilya "orangy" Ryzhenkov [announced](https://twitter.com/orangy/status/216127804482404352) via twitter that JetBrains are bringing on board the team behind the [Nemerle](http://nemerle.org/)Â programming language. This happened a few days after hinting on twitter that a major announcement is coming.

<!-- more -->

The Nemerle language has gotten quite a bit of attention lately. There had been [3 sessions](http://vimeo.com/ndcoslo) about the language at the latest Norwegian Developers Conference (NDC), a .[NET Rocks! episode](http://dotnetrocks.com/default.aspx?showNum=704), and the tooling for Visual Studio 2010 is now also available to the public since version 1.1.

But the most interesting part about this new partnership comes from a [forum post](http://rsdn.ru/forum/nemerle/4789575.1.aspx) (in Russian) of [VladDQ](https://twitter.com/vladdq), one of the main developers, where he talks about JetBrains' plans. One particular mention is that most efforts will be put in a project called N2. There isn't much information available on N2 in English, but [this article](http://rsdn.ru/article/nemerle/N2/N2-Project.rsdnml.xml) in Russian details exactly what it is &#8211; aÂ languageÂ framework built on top of Nemerle, that allows easily creating grammars for any programming language (C#, Nemerle, Java, Delphi, C++, F#, etc.) using a specialized DSL, and N2 would generate parsers, unit tests, refactoring support and IDE integration automatically!

But what makes this most exciting is this quote from VladDQ, from the middle of the page (machine translation):

> N2 will be integrated with ReSharper, so that all languages are made based on it, get automatic support for IDE and the ability to create their own refactorings.

**Edit:** Here is a [translation](https://groups.google.com/forum/#!msg/nemerle-en/LKkEcftHF9I/7ANd0PDwSnEJ) of the forum post.

If I understand this correctly, this means that N2 will become the "core" language service of ReSharper, which would make it very easy to add tooling support (read: ReSharper support) for new languages, and extend existing ones, simply by implementing the N2 DSL!

Of course, this is all speculation on my part, and we will know more once the "official" information begins to appear on the JetBrains tools blog. But I hope I am right &#8211; in which case, JetBrains + Nemerle = truly the most exiting news in developer tooling lately!
