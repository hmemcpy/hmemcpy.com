---
title: Supercharging your ReSharper navigation-fu with Camel Humps
date: 2011-05-09T01:30:34+00:00
---
I blog about <a href="http://www.jetbrains.com/resharper/" target="_blank">ReSharper</a> a *lot*, mostly due to it's being an awesome product which greatly improves my productivity. One of the major tips any ReSharper user is given &ndash; use the keyboard shortcuts. A lot. Some even go completely mouseless!

<!-- more -->

Here's a little tip to make navigation your code even better: <a href="http://blogs.jetbrains.com/dotnet/2008/02/resharper-in-detail-camelhumps/" target="_blank">CamelHumps</a>. CamelHumps is a ReSharper feature that allows navigating and selecting parts of compound names, according to <a href="http://en.wikipedia.org/wiki/CamelCase" target="_blank">camelCase</a> rules, so that if you have a method named `CreateUser_WithValidUsernameAndPassword_UserIsCreated` (like I name my unit tests, `UnderTest_Scenario_ExpectedResult`), with CamelHumps enabled, you would be able to move the caret to the beginning of every word using **Ctrl-Left/Right**.

While this is a great feature, I wouldn't want it enabled all the time, since it's also affects Extend/Shrink Selection (Ctrl-W), which sometimes can be annoying. Fortunately, those actions are available as Visual Studio actions, so they can be used even if CameHumps is turned off globally:

  * _ReSharper_HumpNext_ &#8211; move caret to next hump/word
  * _ReSharper_HumpPrev_ &#8211; move caret to previous hump/word
  * _ReSharper_HumpNextExtend_ &#8211; expand selection to next hump
  * _ReSharper_HumpPrevExtend_ &#8211; expand selection to previous hump

I recommend binding the _ReSharper_HumpNext_ and _ReSharper_HumpPrev_ to **Alt-Right** and **Alt-Left**, and _ReSharper_HumpNextExtend_ and _ReSharper_HumpPrevExtend_ to **Alt-Shift-Right** and **Alt-Shift-Left**, respectively. Make sure you select **Text Editor** under *Use new shortcut in* in Tools &ndash; Options &ndash; Keyboard, or your binding might not work.

**Please note:** the later binding breaks the <a href="http://weblogs.asp.net/scottgu/archive/2010/04/26/box-selection-and-multi-line-editing-with-vs-2010.aspx" target="_blank">Box Selection</a> feature in Visual Studio 2008, however greatly improves it in Visual Studio 2010 &ndash; it makes box selection respect the camelCase as well!

Here's how it works &ndash; let's say I want to rename the word _Spelling_ to _Proofreading_ in the method name, and the caret is inside the method body:

**Step 1:** Press **Ctrl-[** to jump to containing method (jumps to start of the method name)
{% asset_img image1.png %}

**Step 2:** Press **Alt-Right** a few times to jump to the beginning of the word Spelling
{% asset_img image2.png %}

**Step 3:** Press **Alt-Shift-Right** to select the word Spelling
{% asset_img image3.png %}

I'm using <a href="http://osherove.com/" target="_blank">Roy Osherove's</a> excellent <a href="http://osherove.com/blog/2007/6/3/train-to-be-a-keyboard-master-with-keyboard-jedi.html" target="_blank">Keyboard Jedi</a> utility to demonstrate the keyboard shortcuts. Unfortunately it doesn't work on a 64-bit Windows, but you can fix it with this <a href="http://codebetter.com/jameskovacs/2008/04/25/keyboard-jedi-on-vista-x64/" target="_blank">little hack</a> by <a href="http://jameskovacs.com/" target="_blank">James Kovacs</a>.

Unfortunately, this doesn't work in the rename dialog (and others). There's a 3-year old <a href="http://youtrack.jetbrains.net/issue/RSRP-40844" target="_blank">issue</a> reported on the ReSharper's Issue Tracker about this, however it hasn't been added yet. Maybe it's time, guys?
