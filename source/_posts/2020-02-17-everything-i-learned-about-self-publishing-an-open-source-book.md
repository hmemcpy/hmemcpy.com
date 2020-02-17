---
title: Everything I learned about self-publishing an open-source book
date: 2020-02-17 12:03:11
---

Over the past two years, the PDF version of Bartosz Milewski's [*Category Theory for Programmers*](https://bartoszmilewski.com/2014/10/28/category-theory-for-programmers-the-preface/) became a highly-successful [open-source book](https://github.com/hmemcpy/milewski-ctfp-pdf), which was adapted to other programming languages, such as Scala and OCaml. There was a high demand for a physical copy of the book, so I went exploring the vast options, which I summarize below.

<!-- more -->

The book is published under a [Creative Commons Attribution-ShareAlike](https://creativecommons.org/licenses/by-sa/4.0/) (CC-BY-SA), a license that allows free sharing and modification of the book. For that reason, I wanted to minimize the cost of publishing the book, and choose a self-publishing route. Here are the things I learned along the way, in no particular order:

#### Print-on-demand

There are several print-on-demand (POD) [services to choose from](https://blog.reedsy.com/print-on-demand-books/): Lulu, Blurb, BookBaby, KDP (Kindle Direct Publishing), and IngramSpark. My requirements were: hardcover availability and a color print (because the book drawings are too adorable!), some services do not provide either or both of those options.

Most POD services have a calculator that allows *guesstimating* the final cost, depending on the number of pages, choice of paper, whether it's a hard or softcover, book size, and other parameters. I ended up choosing Blurb because they offer a [hardcover print in economy color](https://www.blurb.com/trade-books) significantly cheaper than the alternatives. For black-and-white books, Lulu is also a very good option.

I also did quite a bit of research regarding the final quality of the book. There are posts [comparing various samples](https://medium.com/@mwichary/my-experiences-printing-a-small-batch-of-books-c04141b63dfe), as well as video reviews on YouTube. Depending on your requirements, you may want to experiment with a smaller-size manuscript to determine the quality of your book.

Most POD services will handle everything, from uploading the manuscript to distribution, providing you (in most cases) a free ISBN (a number, required for listing your book in online and brick-and-mortar bookstores). However, the options for book dimensions and paper quality may be limited. One exception is [IngramSpark](https://www.ingramspark.com/), a POD service that offers a high degree of customization, but at a more expensive cost.

#### Book sizes and dimensions

Most POD services offer a standard size for trade books at 6×9" (15×23 cm) and 8×10" (20×25 cm). Most technical books in my bookshelf (with an occasional oddity) are sized 6×9", which is the size I chose. Blurb and others provide exact specifications for the paper and cover sizes needed for the print. Some provide a [specifications calculator](https://www.blurb.com/make/pdf_to_book/booksize_calculator), allowing you to get the exact measurements for your book, including the *bleed* and *trim* lines. Others offer Adobe Publisher templates and custom tools. This step requires a lot of experimentation, as the final result may only be visible in the previewer of the particular service. And even then, the actual printed copy may contain slight variations.

To set the dimensions in LaTeX, there are packages like `geometry`, if using a `\documentclass{book}`, and the `\documentclass{memoir}` allows additional arguments for specifying height, width, margins, bleed, and other parameters. Also, the [`crop`](https://ctan.org/pkg/crop) package is a useful diagnostic tool, allowing cropping the pages at specified sizes for a better preview.

The process of uploading a PDF and previewing it online before publishing varies between the POD services, but most offer a nice experience for it. However, the absolute final result can only be experienced by holding the physical copy in your hand. Some services, like Lulu, will send you a draft copy for free, before the final approval. Blurb does not offer this, and you will have to purchase a copy yourself. Other services may provide different terms.

Some examples of specifying LaTeX dimensions for a 6×9" print can be found in online open-source books, like [HoTT](https://github.com/HoTT/book/blob/29279f5d00f1fdb013d5c7fbe804b49cb25e61b1/opt-ustrade.tex), [OpenLogic Project](https://github.com/rzach/forallx-yyc/blob/master/forallxyyc-print.tex), and, of course, the [book by yours truly](https://github.com/hmemcpy/milewski-ctfp-pdf/blob/master/src/preamble.tex).

#### Publishing on Amazon

To have your book listed on Amazon (and other online and offline stores), it requires additional price markup on your book (Amazon requires a 15% markup on the price, as well as a $1.35 distribution fee for each book). Most POD services offer distribution on Amazon, allowing you to configure the list price in the book settings of your dashboard.

One exception is KDP (Kindle Direct Publishing), which is an Amazon POD service (formerly CreateSpace). It allows publishing books directly on Amazon and even offers a wider range of available sizes and other options. Unfortunately, at the time of writing, Amazon KDP does not offer a hardcover print. 

As a data point, Fabien Sanglard, the author of [Doom: Game Engine Black Book](https://twitter.com/fabynou/status/1121093556720979969) breaks down the price of publishing his book [on his site](http://fabiensanglard.net/gebbdoom/).

In my case, I opted not to list the book on Amazon, and offer it directly via the publisher. The price remains just the cost of printing and orders and shipping are handled via the publisher.

#### Publishing and updating

Some more details about the process of uploading and listing the book. On Blurb, the process starts by [uploading the PDF](https://www.blurb.com/pdf-to-book), as well as an additional cover PDF (alternatively, the cover may be included in the same PDF on the first and last pages). The file will be uploaded and processed by Blurb, scanned for any issues with size and quality. In some cases, it can automatically fix issues it encounters. 

After uploading is done, it's possible to preview the book online. This step is crucial for finding any alignment issues and verifying exact dimensions.

Finally, the book will appear in the dashboard, allowing you to configure metadata, such as author, description, category, etc., as well as setting a listing price of your choosing.

A downside of this process is that each new upload generates a new entry, with a new permalink to the book. Blurb does not allow replacing existing book content with a new PDF. It does, however, offer a [writing tool](https://www.blurb.com/bookwright) that allows you to write the book, and submit as many revisions as needed.

Other publishers, like Lulu, do allow you to modify the book after it was uploaded. This may be a better option if you need to keep the book information up-to-date.

#### Using a publisher

The self-publishing route is a good solution if you prefer to work at your own pace and control all aspects of the process. You are, however, responsible for editing, proofreading, cover design, distribution, and, in some cases, registering trademarks and ISBNs. 

These services may be provided to you by an established publisher, such as Manning or Apress. They take care of the entire process, from editing to wide distribution. Publishers such as No Starch Press are always looking for new authors, so it may be wise to check about the possibility of publishing your book with them.

Happy writing!
