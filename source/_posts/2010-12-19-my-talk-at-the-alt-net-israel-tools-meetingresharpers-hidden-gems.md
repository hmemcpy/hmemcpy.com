---
title: My talk at the ALT.NET Israel Tools meeting - ReSharper's Hidden Gems
date: 2010-12-19T12:13:11+00:00
---
I was delighted to talk about [ReSharper](http://www.jetbrains.com/resharper/) at the recent meeting of the [ALT.NET Israel](http://groups.google.com/group/altnetisrael) group. I chose ReSharper for the reason that I use it every day, and I can't imagine myself programming without it. I wanted to share with the rest some tips, tricks and general hidden features of this wonderful tool that I've learned over the years using it.

<!-- more -->

ALT.NET Tools meetings are series of short demos (about 20 minutes per speaker). It was my first time speaking to a large group of people, and I wasn't sure if I could keep their attention. I ended up giving a good 40 minute talk, and managed to wow everyone in the room during the process!

For the demo I used the following: ReSharper 5.1 (I used the latest [nightly build](http://confluence.jetbrains.net/display/ReSharper/ReSharper+5.1.2+Bugfix+Builds), however the official release is recommended), [Agent Smith Plugin](http://code.google.com/p/agentsmithplugin/) (an open-source code style validation plugin for ReSharper) and Philip Laureano's [LinFu](http://www.codeproject.com/KB/cs/LinFuPart1.aspx) as the demo project.

  * ### nguid

The first feature that I demonstrated was a [live template](http://www.jetbrains.com/resharper/features/code_templates.html#Live_Templates) that comes out of the box, called **nguid**. This allows you to instantly create a new GUID anywhere: in source files, XML/Config files or any text file that is opened within Visual Studio, just by typing **nguid** and pressing the **Tab** key. If you require lots of GUIDs (when working with [WiX Installer](http://wix.sourceforge.net/), for instance), this will save a lot of time by generating new GUIDs on the fly.

  * ### Recently edited

One of my most used features of ReSharper is the ability to navigate to the recent place an edit occurred. By pressing **Ctrl-Shift-Backspace**, you will be immediately taken back to the last place you changed code. Repeat to go back to all places an edit took place. To view a list of all recent files, press **Ctrl-,** (Visual Studio) or **Ctrl-E** (IDEA).
{% asset_img image1.png %}

  * ### Navigating to constructors

I learned this neat trick fairly recently from JetBrains' own [Hadi Hariri](http://hadihariri.com/), while looking for interesting topics to discuss at the meeting. In any code file, type **new** into the *Go To File Member* navigation (**Alt-/** [Visual Studio] or **Ctrl-F12** [IDEA]), and it will list all constructor first!
{% asset_img image2.png %}

  * ### Working with Solution-wide analysis

I wrote about the benefits of turning Solution-wide analysis back when I [reviewed ReSharper 4.5 Beta](/2009/03/resharper-4-5-beta-released/). Several things happen when Solution-wide analysis is enabled &ndash; all public and protected methods are now analyzed for usage and visibility. This allows, for instance, making public methods private (if they are unused outside the class), or removing them completely, if they aren't used at all.

{% blockquote %}
A word of caution when changing visibility (or even removing) unused public classes &ndash; make sure that your code is not being called dynamically (i.e. via MEF, or reflection). ReSharper will not detect such usage, and you might end up with broken references.
{% asset_img image12.png %} {% asset_img image13.png %}
{% endblockquote %}

Another important benefit of working with Solution-wide analysis enabled is the ability to immediately detect errors in the entire solution, rather than just the current file. The Next/Previous error navigation (**Shift-Alt-PgDn/PgUp** [Visual Studio] or **Alt-F12/Shift-Alt-F12** [IDEA]) will now take you to all errors in your solution.

  * ### Code issues inspection

At this point I was asked if there was a way to list all ReSharper hints, suggestions and warnings &ndash; indeed there is, and it's called *Code Issues*. It's available from ReSharper's _ReSharper &#8211; Inspect_ menu, in form of *Code Issues in Current Project* or *Code Issues in Solution*. Depending on the size of your solution, the initial analysis of all your files might take a few minutes (this is reduced greatly if Solution-wide analysis is enabled). After the wait, all ReSharper's suggestions are presented in a tool window:
{% asset_img image3.png %}

  * ### SSR (Structural Search and Replace) and Patterns Catalog

The next thing I talked about is the SSR. I wrote about SSR [previously in greater detail](/2010/02/resharper-5-hidden-gem-patterns-catalogue/), and I demonstrated how to convert [NUnit's](http://www.nunit.org/) Assert syntax to its fluent API. I also demonstrated how to [use Agent Smith Plugin to document the public API](/2010/11/documenting-your-public-api-easily-with-resharper-and-ghostdoc/).

  * ### **ReSharper.Internal**

<span style="color: red;">**THE FOLLOWING IS AN UNDOCUMENTED, UNSUPPORTED FEATURE OF RESHARPER. USE THIS AT YOUR OWN RISK!**</span>

Before I even started my talk, I asked the audience who used ReSharper to raise hands. Of almost 40 people, I think 90% raised their hands. I guaranteed them that the feature I was about to show was something they never heard of before, and I was pleased to have been right!

ReSharper's *Internal Mode* (or *God-mode* or *<a href="http://doom.wikia.com/wiki/Doom_cheat_codes">iddqd</a>*, as it was referred to around the room) is an internal set of tools and commands, used mostly by ReSharper developers at JetBrains. To enable it, start Visual Studio with the following command line switch:

`devenv.exe /ReSharper.Internal`

You will now have a new menu in ReSharper's menu called _Internal_. There are many things available here, some of which are of no use to anyone outside JetBrains. I am going to show two most useful ones.

#### PSI Browser and PSI Viewer

PSI (Program Structure Interface) is JetBrains implementation of Visual Studio's AST (Abstract Syntax Tree). It allows representing every single construct of a source file in a syntactic tree. These tools are an indispensible aid for plugin developers, for instance, when trying to understand the structure of the source code.

PSI Browser (located under _Windows_) displays the entire structure of the currently opened file. By double clicking any element, it will jump to the corresponding place in the source code.
{% asset_img image4.png %}

PSI Viewer is a great utility to create code snippets on the fly, and view their PSI representation.
{% asset_img image5.png %}

#### Concurrent building with MSBuild

After turning on Internal mode, upon trying to build the solution for the first time, you will be presented with the following dialog:
{% asset_img image6.png %}

By selecting MSBuild, ReSharper will build the solution using MSBuild, rather than the Visual Studio builder. One advantage MSBuild has over Visual Studio is the ability to utilize multiple cores of the CPU to build the solution concurrently. This is disabled by default, to enable it, go to _ReSharper &ndash; Options_. The options dialog will look slightly different when Internal mode is enabled. Menu items having a green circle on their right are only available in Internal mode. Scroll all the way down, under *Tools*, and select the *Internal* menu. On the right side make sure that the highlighted items are checked:
{% asset_img image7.png %}

Since MSBuild is not integrated into Visual Studio, when building you will not be able to see the build progress in the output window. The project status view is a tool window which shows all the projects in solution (abbreviated), and displays their build progress by using colors.
{% asset_img image8.png %}

Please note that this is an experimental build technique, and it might not work correctly for your solution. Like all other features above, use this at your own risk.
