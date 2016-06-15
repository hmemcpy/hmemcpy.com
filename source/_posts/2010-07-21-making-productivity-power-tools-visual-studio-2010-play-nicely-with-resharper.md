---
title: Making Productivity Power Tools for Visual Studio 2010 play nicely with ReSharper
date: 2010-07-21T21:02:02+00:00
---
Scott Guthrie [wrote](http://weblogs.asp.net/scottgu/archive/2010/07/19/vs-2010-productivity-power-tools-update-with-some-cool-new-features.aspx) about VS 2010 Productivity Power Tools update, and I went to the Extensions Gallery to download it. I won't write an overview about it, ScottGu has already done an excellent job on [his blog](http://weblogs.asp.net/scottgu/archive/2010/07/19/vs-2010-productivity-power-tools-update-with-some-cool-new-features.aspx). You can also find more information on the [extension's page](http://visualstudiogallery.msdn.microsoft.com/en-us/d0d33361-18e2-46c0-8ff2-4adea1e34fef).

<!-- more -->

If you're a [ReSharper](http://www.jetbrains.com/resharper/) addict (like me), you will notice that some things just do not work or interfere with the way ReSharper does things. So here's a list of things that you can do to make ReSharper and the Productivity Power Tools work nicely together:

Go to the Productivity Power Tools under **Tools &ndash; Options**:
{% asset_img image1.png %}

  * Turn off **Automatic Brace Completion** if you prefer ReSharper to do it for you.
  * Turn off **Ctrl + Click Go To Definition**. ReSharper provides this functionality.
  * Turn off **Move Line Up/Down Commands**. This breaks ReSharper's equivalents.
  * Turn any other settings on or off, depending on your personal preferences.

#### Fixing Quick Access

One of the best features of the Productivity Power Tools is the **Quick Access** window. If you're a ReSharper user, you'll appreciate it if you love the **Go To Class** navigation (Ctrl-**T** [Visual Studio] or Ctrl-**N** [IntelliJ]). The **Quick Access** allows you to navigate virtually everywhere by typing the name. For example, to open the Keyboard options, simply start typing **keyb:**
{% asset_img image2.png %}

The default shortcut for this window is **Ctrl + 3**, however this key binding is used by ReSharper's Bookmarks system. If you're not using the bookmarks:

  * Go to **Tools &ndash; Options &ndash; Keyboard**, find the command by typing **QuickAccess**. You should see it in the list as `View.QuickAccess`.
  * Under **Use new shortcut in** make sure it shows **Global**, then press **Ctrl+3** (without the + sign) in the adjacent text box, then click **Assign**.
  * Select **Text Editor** in the **Use new shortcut** and repeat the above step.

There are many more cool features in these Power Tools. Together with ReSharper they really boost productivity sky high!

Happy coding!
