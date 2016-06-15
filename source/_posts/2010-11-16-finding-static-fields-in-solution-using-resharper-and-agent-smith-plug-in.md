---
title: Finding static fields in solution using ReSharper and Agent Smith plug-in
date: 2010-11-16T14:49:36+00:00
---
Today I came across a need to find all static fields in my entire solution I'm working on. Finding things usually is a no-brainer with [ReSharper](http://www.jetbrains.com/resharper/), but this time I didn't find an option to do this easily.

<!-- more -->

[Agent Smith plug-in](http://code.google.com/p/agentsmithplugin/) is an open-source code-style validation plug-in for ReSharper, which greatly complements ReSharper's own code-style validation, by adding additional (and custom) checks. There are many other useful features of this plug-in, such as the spell checker for just about everything (string literals, XML comments, method names, etc.). Another greatly useful feature is the XML comment validator.

> **Tip for fresh install of the plug-in:** it comes with a bunch of default naming validation rules, which might conflict with those defined by ReSharper. It's best to turn them off by unchecking them in **Languages &ndash; C# &ndash; Naming Convention Settings** in ReSharper options dialog.

There's a trick I learned some time ago &ndash; using Agent Smith's XML comment validation to find undocumented functions in a public API. The same trick can be applied to finding static fields, and here's how:

**Option 1: using Code Issues Inspection**

First, ensure that XML validation inspection is enabled; in ReSharper's options, under **Code Inspection &ndash; Inspection Severity**, look for **Agent Smith**, and make sure that *Members must have XML comment.* is set to at least *Show as suggestion*.

Go to **Languages &ndash; C# &ndash; Agent Smith Code Style Settings**, optionally remove existing rules on the left hand side, then press **Add** to add the following rule:
{% asset_img image1.png %}

The dialog above will create the rule *Any static not readonly field*, which is exactly what I am looking for. Press OK, and close the Options dialog.

We're done with Agent Smith, now it's time to run another hidden gem of ReSharper &ndash; Code Issues Inspector. Go to **ReSharper &ndash; Inspect &ndash; Code Issues in Solution**. Your solution will be analyzed for any code issues which you might have (all based on ReSharper's inspection severity levels). This might take a few minutes, depending on the size of your solution. After the analysis, the Inspection Results window will open, showing you (potentially thousands) of results.

Press *Filter Issues* button (first button on the right), uncheck all inspections, keeping only Agent Smith's *Members must have XML comment.* You will end up with the following:
{% asset_img image2.png %}

And that's it &ndash; a list of static fields in the entire solution is presented.

**Option 2: using Solution-wide analysis**

If you have **Solution-wide analysis** enabled (the little circle at the bottom right corner of Visual Studio), mark *Members must have XML comment.* as *Show as error* in Inspection Severity settings. This will cause all matching static fields to appear as errors in the solution, and then you can navigate them using **Shift-Alt-PgDown/PgUp** (ReSharper keymap) or **Alt-F12/Shift-Alt-F12** (IntelliJ keymap).

Happy hunting!
