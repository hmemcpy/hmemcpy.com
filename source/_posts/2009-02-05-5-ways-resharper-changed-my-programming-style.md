---
title: 5 ways ReSharper changed my programming style
date: 2009-02-05T12:35:38+00:00
---
I love [ReSharper](http://www.jetbrains.com/resharper/). It has completely changed the way I think about code. When I have to use Visual Studio without ReSharper installed, I feel like I'm writing the code in Notepad. As my first actual post on this blog I'd like to present a _few_ features of ReSharper 4.1 that help me code faster, better, (stronger) and with much higher accuracy.

<!-- more -->

Here are a few things I _don't_ do anymore:

**1. Look for files in Solution Explorer**

Gone are the days when I have to take my hands off the keyboard to use the mouse to find a file deep in the Solution Explorer. If I have to find a type, I use **Go To Type** (Ctrl-**T** [Visual Studio] or Ctrl-**N** [IntelliJ]):
{% asset_img image.png %}

Usually that's enough, since I almost always know the type name I'm looking for, otherwise I'd look for the file itself using **Go To File** (Ctrl-Shift-**T** [Visual Studio] or Ctrl-Shift-**N** [IntelliJ]):
{% asset_img image1.png %}

Another great feature of those options is acronym support. For example, I can quickly navigate to **WebDavMethodLogger** class by typing **WDML** (if the type name is Pascal Cased), or **wdml** in lowercase:
{% asset_img image2.png %}

More interesting Go To navigations: **Go To Symbol** (Alt-Shift-T [Visual Studio] or Ctrl-Alt-Shift-**N** [IntelliJ]), **Go To Member** (Alt- [Visual Studio] or Ctrl-**F12** [IntelliJ]).

**2. Manually create constructors, fields, properties**

Meet one of my best friends &ndash; **Generate** (Alt-Insert). Pressing this shortcut anywhere in the file will popup this menu:
{% asset_img image3.png %}

If I select **Constructor** from the menu, I'll get a dialog in which I'll be able to specify constructor parameters, and automatically map them into local fields.

Let's say you've made an empty class *Person*, and manually typed out the following:
{% asset_img image4.png %}

Notice two things here: the parameter names **name** and **lastName** are grayed out. It means that they are not (yet) used anywhere in our class. Also, notice the red bulb on the left side? That is my other best friend &#8211; the **Action** (Alt-Enter) key. Pressing Alt-Enter when will give this menu:

{% asset_img image5.png %}
Few keystrokes later, and I have the following code:

{% asset_img image6.png %}
The Action key presents contextual actions, such as removing unused methods, split/join variable declarations, turn string concatenations into **string.Format, **where they are applicable, and many more.

**3. Rebuild the solution to find errors/making sure the code compiles**

I wonder how many years have been spent watching the code trying to compile, only to get a nice list of errors with different reasons why it can't. ReSharper provides visual cues to things that are wrong with your code:
{% asset_img image7.png %}

Notice the little red lines on the scroll bar (on the left). These are compilation errors in the code. ReSharper analyzes the code as you type, and displays errors immediately. You can hover above them with the mouse, and the hint will show what's wrong. To navigate to the error, click with the mouse, or better use the **Go To Next Error** (Shift-Alt-PgUp/PgDown [Visual Studio] or Alt-**F12**/Shift-Alt-**F12** [IntelliJ]) key.

The red circle in the status bar shows total files with errors in the entire solution. If this is turned on (disabled by default in new solutions), the same shortcut will navigate to the errors in the entire solution.

Other visual clues are Word-like squiggly lines under the used to describe other miscellaneous errors, warnings and suggestions.

**4. Use text search/find references to navigate interfaces and abstract class implementations**

One of the most useful features that ReSharper provides is navigation to implementers from base classes, and vice-versa. By using **Navigate from Here to** (Alt-`) I get a popup which allows to quickly navigate to all implementations:
{% asset_img image8.png %}

I can also go to the definition of the type by performing **Ctrl-Left click**, or pressing **F12** [Visual Studio] or Ctrl-**B** [IntelliJ] on the type name in the code.

**5. Move code around by select/drag-drop or copy/paste**

Sometimes I need to re-arrange methods within the class. Instead of selecting the code with the mouse and then cut/paste it, I use **Move code Up/Down** (Ctrl-Shift-Alt-Up/Down) when my caret is on on the method name. Same shortcut works when trying to move code lines within the method. If I need to select some portions of my method, I use **Extend selection** (Ctrl-W) which selects just the parts of the code I need. If I select too much, I can use **Shrink selection** (Ctrl-Shift-W).

This is a very small subset of features that make ReSharper. It's a wonderful addition that makes my job much easier. Sure, it takes time to get used to and configure properly, but once it's configured to suit all your need, you'll never want to continue writing code without it.