---
title: 'Using #regions in XAML (yes, really!)'
date: 2012-10-30T12:15:04+00:00
---
<img style="background-image: none; float: right; padding-top: 0px; padding-left: 0px; margin: 0px 0px 0px 5px; display: inline; padding-right: 0px; border-width: 0px;" title="" src="http://i0.wp.com/hmemcpy.com/wp-content/uploads/2012/10/457236971_3abe1f2afb.jpg?resize=244%2C184" alt="" align="right" border="0" data-recalc-dims="1" />Let's get this out of the way first: I **_hate_** [#regions](http://msdn.microsoft.com/en-us/library/9a1ybwek.aspx)! It's a construct that was introduced to C# 1 to help separate generated code in WinForms from the actual user code (there was no support for .Designer or partial classes yet). Regions became an abuse, where developers would simply _hide_ huge code behind regions, instead of following SRP and keeping classes small. I actually [voted](http://youtrack.jetbrains.com/issue/RSRP-305779) and [suggested](http://youtrack.jetbrains.com/issue/RSRP-330110) that ReSharper will not generate any regions by default.

<!-- more -->

Having said that, however, if there is one thing that is worse than regions is huge XAML files. Being very verbose, XAML tends to get huge, even for the most simple things, and it becomes very difficult to navigate and read.

Turns out, someone made an extension for Visual Studio called [XAML Regions](http://visualstudiogallery.msdn.microsoft.com/3c534623-bb05-417f-afc0-c9e26bf0e177), which allows adding regions in .xaml files with an XML comment-like syntax:

<pre>&lt;!-- Region (Any Text You Want) --&gt;
Your Code
&lt;-- EndRegion --&gt;</pre>

Which lets you collapse blocks of XAML code:

<img src="http://i2.wp.com/visualstudiogallery.msdn.microsoft.com/site/view/file/46783/1/XAMLRegionsBig.png?w=900" alt="" data-recalc-dims="1" />

To make this even easier, let's create a ReSharper Live Template to help surround our XAML with a XAML region:

  * Open Templates Explorer under ReSharper menu
  * Select **Surround Templates**
  * Under **Scopes**, select **XML** and press the **New Template** button
  * Write the following:

![](http://i2.wp.com/hmemcpy.com/wp-content/uploads/2012/10/SNAGHTML56004f2.png)

  * Drag the new snippet, **region**, into the _**In Quicklist**_ category:

![](http://i2.wp.com/hmemcpy.com/wp-content/uploads/2012/10/SNAGHTML5a7c802.png)

From now on, you can use the **Surround With** (**Ctrl-E,U** in Visual Studio bindings, **Ctrl-Alt-J** in IDEA bindings):

![](http://i2.wp.com/hmemcpy.com/wp-content/uploads/2012/10/image82.png)
