---
title: ReSharper 5.0 Hidden Gem - Patterns Catalogue
date: 2010-02-25T21:06:26+00:00
---
**[November 16, 2010]** While the information below is still very much relevant, please download the latest version of [ReSharper](http://www.jetbrains.com/resharper/) from JetBrains website.

Have I mentioned that I love ReSharper? While patiently waiting for the 5.0 release to RTM, the team at JetBrains have shipped the [Beta 2 release](http://www.jetbrains.com/resharper/beta/beta.html) (build 1618). This is a very stable, very good improvement over the previous [nightly builds](http://confluence.jetbrains.net/display/ReSharper/ReSharper+5.0+Nightly+Builds).

<!-- more -->

One of the things that improved the most with this release is the SSR &ndash; Structural Search and Replace. It's a new feature, allowing you to specify code patterns to be added as hints, errors or warnings to the ReSharper code analysis, as well as specifying a replacement pattern.

Here is an [example](http://blogs.jetbrains.com/dotnet/2010/02/resharper-5-beta-2-released/) of this feature, taken from the [JetBrains .NET Tools blog](http://blogs.jetbrains.com/dotnet/):

Adding the following pattern:

![](http://i2.wp.com/blogs.jetbrains.com/dotnet/wp-content/uploads/2010/02/search_replace_pattern.png)

Will add a new quick-fix action:

![](http://i2.wp.com/blogs.jetbrains.com/dotnet/wp-content/uploads/2010/02/ssr_quick-fix.png)

The patterns can also be imported/exported as XML files, allowing easy sharing between co-workers.

In order to create a new pattern, select **Patterns Catalogue** from the **Tools** submenu of **ReSharper** menu.

Press **Add Pattern**.

![](http://i1.wp.com/hmemcpy.com/wp-content/uploads/2010/09/image_9.png)

We can add either a search only pattern, or a search and replace pattern. Let's add a pattern to turn NUnit Asserts into fluent NUnut Assert syntax:

  * Add `Assert.AreEqual($expected$, $actual$)` in the **Search Patten** window.
  * Press **Add Placeholder**, select argument, and type `expected` in the name. Do the same for `actual`.
  * In **Replace Pattern**, type `Assert.That($actual$, Is.EqualTo($expected$))`.
  * Choose Pattern severity, I selected **Show as suggestion**.
  * Fill in the description texts.

The final result should look like this:
{% asset_img image_7.png %}

Press Save and close the Pattern Catalogue dialog.

You will now be able to turn this:
{% asset_img image_13.png %}

into this:
{% asset_img image_16.png %}

Happy coding!
