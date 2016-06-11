---
title: Where unit testing fails
date: 2011-06-24T20:34:42+00:00
---
_**Note:** I wrote this post before watching Uncle Bob's excellent NDC 2011 talk called [Transformation Priority Premise](http://cleancoder.posterous.com/the-transformation-priority-premise), which talks exactly about the subject below, however I am still not convinced. I will write a follow-up to this post._

I remembered a story from a few years ago about *some guy* who tried to build a Sudoku solver using TDD (Test Driven Development) five times, failing and giving up, while *another guy* simply wrote a solver that worked.

<!-- more -->

A search led me to a thread on reddit, leading to <a href="http://ravimohan.blogspot.com/2007/04/learning-from-sudoku-solvers.html" target="_blank">this post</a> by Ravi Mohan. As it happens, *some guy* who tried the TDD approach was <a href="http://en.wikipedia.org/wiki/Ron_Jeffries" target="_blank">Ron Jeffries</a>, one of the fathers of Extreme Programming (XP), while the *other guy* was an algorithm and AI expert <a href="http://en.wikipedia.org/wiki/Peter_Norvig" target="_blank">Peter Norvig</a>. I highly recommend reading the original post and the updates, it makes for very thought provoking read (the original links to Ron Jeffries' articles are broken, but you can find them by searching for <a href="http://xprogramming.com/index.php?s=sudoku" target="_blank">sudoku</a> on his site).

So what happened? How is it that the very people who preach TDD fail to implement it themselves? I believe the problem lies with grasping one of the most fundamental principles of unit testing, and that is &ndash; what _not_ to test.

In one of the Software Craftsmanship Israel group meetings, our programming task for the evening was to implement a program that detects whether a given number was a <a href="http://en.wikipedia.org/wiki/Lychrel_number" target="_blank">Lychrel number</a>. On the projector screen a summary of what a Lychrel number was, and some samples. We decided to split into pairs of people who knew how to write code using TDD (myself included), and people who were less experienced in writing tests. And so we began*¦

> A Lychrel number is a number that does not form a <a href="http://en.wikipedia.org/wiki/Palindrome" target="_blank">palindrome</a> when digits are reversed and then added together iteratively. For example: 56 + 65 = 121, 125 + 521 = 646, therefore both not Lychrel numbers. The smallest suspected Lychrel number is 196, failing to form a palindrome after more than 2 million iterations. This is also known as 196-algorithm.

Some 30 minutes passed before I realized that something didn't feel right. We had written almost 10 test cases, all of which just asserted against known inputs and outputs we used from the projector screen. Several of us started arguing whether or not we should test the method `IsPalindrome`, since it was an implementation detail, and not a part of the interface.

I then remembered the story about the Sudoku solver and it made sense to me, just as it made sense to Vlad Levin &ndash; <a href="http://vladimirlevin.blogspot.com/2007/04/tdd-is-not-algorithm-generator.html" target="_blank">TDD is not an algorithm generator</a>! The solution to the Lychrel number had just one solution &ndash; implementing the algorithm. There was no design that was needed, therefore TDD did not help in this case. All it had given us was a convenient way to input values to a function and getting a result.

At <a href="http://www.typemock.com/" target="_blank">Typemock</a> where I work I am sometimes asked via support how to test the DataSet or the DataReader, and whether our product can be used to mock the database. Yes, Typemock Isolator can be used to mock just about any object, the question is asking the wrong thing. You _could_ create a fake DataReader filled with test data, but that would be too much work and very hard to maintain, and in the end will give you no benefit over using a real database. If you want to test whether your data access code works correctly &ndash; make it an _integration test_ instead.

When I write unit tests today I try abstract my problem space. I no longer start at the very bottom, but rather I focus on the business requirement. A _unit_ in unit test is not necessarily a method or even a class &ndash; it could be several classes collaborating together to achieve a business requirement. If your specification says *given a country, get an _alphabetized_ list of cities*, don't write tests for the sorting algorithm &ndash; it's an implementation detail that you shouldn't bother testing. Your assert should verify is that the list was indeed alphabetized, not which algorithm was used to sort it.

Many people very new to unit testing sometimes give up. They find it hard to know what to test, and end up spending many hours testing the wrong thing. When it later breaks, they find it too much of a hassle to maintain both the code and the tests, so they give up the later. The road to successful unit testing begins with understanding what unit testing is, but most importantly &ndash; what it isn't.
