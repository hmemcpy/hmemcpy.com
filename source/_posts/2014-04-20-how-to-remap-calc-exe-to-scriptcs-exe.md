---
title: How to remap calc.exe to scriptcs.exe
date: 2014-04-20T19:41:56+00:00
---
Lately I found myself launching [scriptcs](http://scriptcs.net/) more and more to do simple calculations. I half-jokingly said on twitter that I'd better remap `calc.exe` to `scriptcs.exe` on my machine. However it seems that my joke tweet was taken seriously by some people, and I was asked how this was done. So here goes!

<!-- more -->

For this next trick I will use my most favorite Windows trick &ndash; the Image File Execution Options (IFEO). I've blogged about IFEO in the past, it's generally used to allow [attaching a debugger to a process before it starts](/2010/12/how-to-debug-a-process-that-is-crashing-on-startup/), but can also do other useful things, such as replacing the Windows Task Manager with Process Explorer, or even disabling some processes launching, which is useful to [prevent Narrator in Windows 8 from launching](/2012/12/how-to-disable-windows-narrator-appearing-on-win-enter-in-windows-8/) via the Win-Enter key.

So here is how to remap `calc.exe` to launch scriptcs instead. First, locate on your machine where `scriptcs.exe` is installed, as we need the full path. You can use the command `where scriptcs.exe` in CMD to find it. If you don't have `scriptcs.exe` in path, best [install it via Chocolatey](http://chocolatey.org/) (you're welcome!)

  1. Open the registry editor (regedit.exe), and navigate to: 
    `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options`

  2. Create a new key called `calc.exe`
  3. Inside the newly created key, create a new **String Value** called **Debugger**
  4. Double-click **Debugger**, and set `c:\path\to\scriptcs.exe -repl` as the value

That's it, from now on when you launch `calc.exe`, `scriptcs.exe` will open instead! To undo this, simply delete the key `calc.exe` from the registry path above.

P.S. if you have Windows SDK installed, you can use the utility `gflags.exe` to do this instead:

  1. Launch `gflags.exe` (need to be launched elevated)
  2. Go to the **Image File** tab
  3. In the **Image** text box, write `calc.exe` and press TAB (I know)
  4. Down at the bottom, under **Debugger**, write `c:\path\to\scriptcs.exe -repl` and press OK

Bonus: now replace `devenv.exe` with `scriptcs.exe`!

Happy hacking!
