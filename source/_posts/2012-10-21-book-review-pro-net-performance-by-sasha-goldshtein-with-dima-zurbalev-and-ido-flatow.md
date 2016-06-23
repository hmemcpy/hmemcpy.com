---
title: "Book Review: 'Pro .NET Performance' by Sasha Goldshtein, with Dima Zurbalev and Ido Flatow"
date: 2012-10-21T11:25:57+00:00
---
<img style="float: left; padding: 5px;" src="http://i1.wp.com/ecx.images-amazon.com/images/I/513bgFFIlfL._SL160_.jpg?resize=121%2C160" />It is often said that all problems in computer science can be solved by another layer of indirection. All, except performance problems. Typically, when performance problems occur, it's best to approach them like peeling an onion &ndash; removing abstractions one by one.

<!-- more -->

Joel Spolsky once wrote that all [abstractions are leaky](http://www.joelonsoftware.com/articles/LeakyAbstractions.html), and when it comes to understanding and solving performance problems, we often times need to understand things beyond the abstraction. Pro .NET Performance takes exactly this approach &ndash; it looks beyond the abstractions the .NET framework provides. Each chapter takes a deep look *under the hood*, into the internals of memory management, object lifetime, reference vs. value types, garbage collection, generic types internals, parallelism and concurrency, unmanaged code, and many more topics, with regards to common performance problems associated with them. This book walks you through the internals of the CLR by utilizing free and commercial tools available, such as CLR profilers, debuggers and other little-known tricks. Pro .NET Performance also has a chapter on algorithm optimization, giving background information on complexity, Big-O notation, Turing machines and NP problems, followed by chapters on performance patterns.

Overall, this book provides very in-depth peek into the internals of the CLR and .NET Framework in general. The author of the book has been teaching and blogging about performance for many years, and now this information is available in this great book, that should be read by anyone who is serious about software development.
