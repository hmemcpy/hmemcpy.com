---
title: How to debug a process that is crashing on startup
date: 2010-12-20T21:51:45+00:00
---
Here's a neat trick which allows you to debug a process by attaching a debugger upon process start. It's useful at times when you can't directly launch an application with debugger attached, or you have a process which accepts command line parameters which are not directly under your control (such as `QTAgent32.exe`, which is the MSTest unit test runner, launched by Visual Studio).

<!-- more -->

[Image File Execution Options](http://blogs.msdn.com/b/greggm/archive/2005/02/21/377663.aspx) is a registry facility which allows you, amongst other things, attach a debugger to an application before its execution. Same trick allows, for example, replacing your Windows Task Manager with [Process Explorer](http://technet.microsoft.com/en-us/sysinternals/bb896653.aspx), or `Notepad.exe` with [Notepad2](http://www.flos-freeware.ch/notepad2.html).

Here's how you set it up:

  * Run `regedit.exe`
  * Go to `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options`
  * Create a new key named as your exe (example: yourprogram.exe)
  * Create a new string value under your exe. The name of the string value is `Debugger`, and the value is `vsjitdebugger.exe`

When you run the executable, you will see the Just In Time prompt asking you to select a debugger:

![Just-In-Time Debugger](http://i2.wp.com/i.imgur.com/CCxJz.png)

Select either an instance of Visual Studio from the JIT selection dialog, or attach with another debugger of your choosing, such as WinDbg, after which press **No** in the dialog to continue executing the process.

Don't forget to remove the registry key once done debugging!
