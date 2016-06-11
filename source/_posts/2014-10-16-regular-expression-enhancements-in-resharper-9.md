---
title: Regular Expression enhancements in ReSharper 9
date: 2014-10-16T02:03:45+00:00
---
Yesterday, JetBrains [announced](http://blog.jetbrains.com/dotnet/2014/10/13/introducing-the-resharper-9-early-access-program/) the first public EAP of ReSharper 9! While I'm sure they will dedicate whole blog posts about the new (and truly amazing!) features of ReSharper 9, I wanted to beat JetBrains to the punch, and let you know about one incredible feature (which I consider a *killer feature* of ReSharper 9). I am talking about the improvements in dealing with Regular Expressions (Regex)!

<!-- more -->

**Update:** read all about the new [Regex support in all its glory on the JetBrains blog](http://blog.jetbrains.com/dotnet/2014/10/27/regular-expression-support-in-resharper-9/)!

There were always 2 ways to write regular expressions in C# code &ndash; either inside one of the methods of Regex class, e.g. `Regex.IsMatch`, or defining a string literal as a constant, and using it in a Regex class later.

ReSharper 9 has **Syntax Highlighting** and **Code Completion** for regex literals! When you start typing a regex into a Regex class, you'll see a list of suggestions, which is being narrowed down as you type:

{% asset_img regex1.png "Code Completion" %}

There's also a special syntax highlighting for the complete regex &ndash; as well as automatic checking for errors:

{% asset_img regex2.png "Syntax Highlighting" %}

However, the *killer feature* is the ability to validate and test the regular expressions straight from Visual Studio! Pressing Alt-Enter anywhere inside the expression will bring the Quick Actions menu, with a new option to **Validate regular expression**:

{% asset_img regex3.png "Regex validation menu" %}

Which opens a new window that lets you input some text to validate your regular expression!

{% asset_img regex4.png "Regex validatior" %}

But the best part of these new enhancements is the ability to transform **any string literal** into a regular expression! Simply press Alt-Enter inside the string literal, and select **Make regular expression here**:

{% asset_img regex5.png "Turn into regex" %}

Will turn into:

{% asset_img regex6.png "With syntax highlighting" %}

And you get all the regex features (validation, intellisense, etc) inside your regex string literals! Amazing!
