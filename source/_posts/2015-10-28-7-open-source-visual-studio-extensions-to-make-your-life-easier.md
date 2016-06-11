---
title: 7 open-source Visual Studio Extensions to make your life easier
date: 2015-10-28T22:15:19+00:00
---
It's time to upgrade your _favorite_ IDE! In this post I will list some of my favorite &#8220;off-the-beaten-path&#8221; extensions for Visual Studio that make my daily tasks much easier. I will not list the obvious ones, such as [ReSharper](https://www.jetbrains.com/resharper/) and [OzCode](http://www.oz-code.com/) (or even [Web Essentials](http://vswebessentials.com/)), but rather few relatively unknown ones that do some very cool things.

Are you ready? Let's begin!

<!-- more -->

# BuildVision

[BuildVision](https://visualstudiogallery.msdn.microsoft.com/23d3c821-ca2d-4e1a-a005-4f70f12f77ba) ([source](https://github.com/nagits/BuildVision)) is an extension that visualizes your build process:

![](https://raw.githubusercontent.com/nagits/BuildVision/master/Screenshots/screenshot1.png)

This little extension shows you the status of your build process, how long it took, and most importantly, errors (if any), that occurred during the build. What's nice about this, is the errors are grouped under each project, so it's much easier to navigate than going through a flat list in the Errors output:

![](https://raw.githubusercontent.com/nagits/BuildVision/master/Screenshots/screenshot4.png)

# Git Diff Margin

[GitDiffMargin](https://visualstudiogallery.msdn.microsoft.com/cf49cf30-2ca6-4ea0-b7cc-6a8e0dadc1a8) ([source](https://github.com/laurentkempe/GitDiffMargin)) adds a margin on the left column (or the scroll bar, if you prefer) of the Visual Studio editor, and shows you the diffs between your changed/deleted lines, allowing you to navigate and revert quickly to the previous change!

{% asset_img git_diff_margin.png "Git Diff Margin" %}

It's a perfect companion to git projects (so, all of them!), and it works very nicely with the Visual Studio Git Provider, if you use it. 

Which brings me to:

# NoGit

[NoGit](https://visualstudiogallery.msdn.microsoft.com/146b404a-3c91-46ff-932a-fb0f8b826f94) ([source](https://github.com/markrendle/nogit)) does one thing and one thing only &ndash; it **disables** the built-in Visual Studio Git source-control provider, which has a habit of re-enabling itself whenever you open a solution that uses git. NoGit will turn off this provider always, whenever a solution is opened.

{% asset_img no_git.png "NoGit" %}

# Reopen Start Page

Another time saver is [Reopen Start Page](https://visualstudiogallery.msdn.microsoft.com/e64380ab-e3aa-4ac7-aa11-95719c5c91e9) ([source](https://github.com/jlattimer/VSReopenStartPage)), which does exactly what it says &ndash; reopens the Visual Studio Start page when you close a solution. Personally, I make use of the recent solutions list on the Start page, which makes it really convenient to open recent solutions!

# SaveAllTheTime

[SaveAllTheTime](https://visualstudiogallery.msdn.microsoft.com/ee676c7f-83e8-4ef8-87ab-22a95ae8f1d4) ([source](https://github.com/paulcbetts/SaveAllTheTime)) is another gem that makes Visual Studio to save changed files and projects ALL THE TIME. Visual Studio sometimes doesn't save project files when you rename or move files around. SaveAllTheTime makes sure everything is saved before you commit your changes!

In addition, SaveAllTheTime contains a small widget, reminding you to commit often. If you're a git power user, or don't use git(ಠ_ಠ), you can disable this widget.

{% asset_img no_git.png "Save All The Time" %}

# TabSanity

I discovered [TabSanity](https://visualstudiogallery.msdn.microsoft.com/ac4d4d6b-b017-4a42-8f72-55f0ffe850d7) ([source](https://github.com/jedmao/tabsanity-vs)) fairly recently, and it was one of those *where has this been all my life!!1* moments. This extension makes tabs-as-spaces behaves like actual tabs! The backspace and delete keys, arrow key navigation will not allow the caret to land within the spaces that form a tab, and it will skip to the next *tab*, saving you keystrokes!

# EmojiVS

Finally, let's add some fun to our code with [EmojiVS](https://visualstudiogallery.msdn.microsoft.com/88575465-8486-4c5a-8406-05e8d1d5b09d) ([source](https://github.com/jbevain/EmojiVS)) &ndash; an extension that adds github emojis to your code (more specifically, code comments). Because, why not?

{% asset_img emojivs1.png "EmojiVS" %}

And it even gives you IntelliSense:

{% asset_img emojivs2.png "EmojiVS in Action" %}

Note: if you're a ReSharper user, you need to install the [ReMoji](https://github.com/hmemcpy/ReSharper.ReMoji) extension _in addition to_ EmojiVS to get code completion.
