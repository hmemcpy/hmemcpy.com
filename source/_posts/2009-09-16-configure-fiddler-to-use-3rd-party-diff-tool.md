---
title: Configure Fiddler to use a 3rd party Diff tool
date: 2009-09-16T07:08:52+00:00
---
I use the awesome [Fiddler2](http://www.fiddler2.com/fiddler2/) to debug HTTP, and I needed to compare sessions. Fiddler has a support for this, but when I clicked **Tools &#8211; Compare Sessions**, it prompted me to install **Windiff.exe**.

<!-- more -->

I haven't found a way to set the [preferred Diff tool](http://www.scootersoftware.com/moreinfo.php) in the UI (via Options), so after looking at the click handler for the menu in [Reflector](http://www.red-gate.com/products/reflector/), I found out that the value can be set via Registry key:

  * Open Registry, go to:

<pre>HKEY_CURRENT_USER\Software\Microsoft\Fiddler2</pre>

  * Add a new String Value called `CompareTool` and set the value to the path of your favorite Diff tool, e.g.:

<pre>"C:\Program Files (x86)\Beyond Compare 3\BCompare.exe"</pre>

<span style="line-height: 1.714285714; font-size: 1rem;"><span style="line-height: 1.714285714; font-size: 1rem;"></span></span>

  * Restart Fiddler

That's it!