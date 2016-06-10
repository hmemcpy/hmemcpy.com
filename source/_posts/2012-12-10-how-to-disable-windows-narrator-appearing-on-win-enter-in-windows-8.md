---
title: How to disable Windows Narrator appearing on Win-Enter in Windows 8
date: 2012-12-10T16:46:53+00:00
---
My colleague was annoyed that pressing Win-Enter on Windows 8 would pop open Windows Narrator, and there was seemingly no way to disable it. He told me that the answer he found on one of the forums suggested [removing the _execute_ permission](http://jake.ginnivan.net/diable-narrator-in-windows-8) from the Narrator.exe file, howeverÂ since this involves preventing file execution, this led me to an idea to try and use my old friend [Image File Execution Options](/2010/12/how-to-debug-a-process-that-is-crashing-on-startup/), which I'm happy to report, worked!

<!-- more -->

  1. Open **regedit.exe** and navigate to: `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options`
  2. Create a folder (key) called **Narrator.exe**
  3. Inside the key, create a new **String value** called **Debugger**, and set its value to **%1**
  4. Close registry editor

From now on, every time Windows will attempt to execute Narrator.exe, nothing will happen!

If you need Narrator.exe back, just remove the **Narrator.exe** registry key.
