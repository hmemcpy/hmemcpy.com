---
title: How to make TestDriven.NET open dotPeek (or any other IL disassembler) instead of Reflector
date: 2011-05-15T11:34:10+00:00
---
[TestDriven.NET](http://testdriven.net/) is a free (for personal use) test runner for Visual Studio, that allows you to run unit tests from the context menu (&#8220;Run Tests*) using any unit testing framework. What I like particularly about TestDriven.NET, is that it allows running or debugging any arbitrary method as well!

<!-- more -->

TestDriven.NET comes with a .NET Reflector integration plugin, allowing you to right-click anywhere in the class and choosing *Go To Reflector*. After the RedGate Reflector fiasco many companies created their own (free) Reflector alternatives. Until Jamie Cansdale (creator of TestDriven.NET) updates his wonderful product to reflect (pun somewhat intended) the changes in the .NET world, here's what you can do to trick TestDriven.NET to open any Reflector alternative: [Image File Execution Options](http://blogs.msdn.com/b/greggm/archive/2005/02/21/377663.aspx).

I [previously wrote](/2010/12/how-to-debug-a-process-that-is-crashing-on-startup/) about using Image File Execution Options to debug a process that is crashing on startup. We can use it to have Windows open any executable when **reflector.exe** is requested:

  * Run `regedit.exe`
  * Go to `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options`
  * Create a new key named **reflector.exe**
  * Create a new string value under **reflector.exe**. The name of the string value is `Debugger`, and the value should be a path to your preferred tool, e.g.: 
    <pre>C:\Program Files (x86)\JetBrains\dotPeek\v1.0\Bin\dotPeek.exe</pre>

Now, when you press *Go To Reflector*, it will open [dotPeek](http://www.jetbrains.com/decompiler/) instead.
