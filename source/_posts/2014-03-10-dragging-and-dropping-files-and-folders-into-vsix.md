---
title: Dragging and dropping files and folders into .vsix
date: 2014-03-10T17:49:44+00:00
---
Visual Studio Extensions, or VSIX files are simple ZIP archives following the [Open Package Conventions](http://msdn.microsoft.com/en-us/magazine/cc163372.aspx), and have a .vsix extension. Double-clicking on a .vsix will install it into Visual Studio, by opening it with VSIXInstaller.exe.

<!-- more -->

**TL;DR:** IF you want to be able to drag files and folders into .vsix, there's a registry tweak you can apply &ndash; add Windows Compressed (zipped) Folders&nbsp; drop handler's GUID to the .vsix entry under HKCR\.vsix. Create the subkeys `shellext\DropHandler`:

<pre>HKEY_CLASSES_ROOT\.vsix\shellex\DropHandler</pre>

Set the value of `(Default)` inside `DropHandler` to `{ED9D80B9-D157-457B-9192-0E7280313BF0}`, restart explorer.exe, and voilla! You can now drag files or folders into .vsix files, as if they were named .zip.

// output:verbose

I wanted to drag some files into the VSIX package, but it didn't work &ndash; Windows has no idea that a .vsix is actually a .zip file:

 <img title="" style="border-left-width: 0px; border-right-width: 0px; background-image: none; border-bottom-width: 0px; padding-top: 0px; padding-left: 0px; display: inline; padding-right: 0px; border-top-width: 0px" border="0" alt="" src="http://i0.wp.com/hmemcpy.com/wp-content/uploads/2014/03/image.png?resize=735%2C346" data-recalc-dims="1" />

Dragging files and folders onto other files or folders is handled by [Shell Drop Handlers](http://www.codeproject.com/Articles/529515/NET-Shell-Extensions-Shell-Drop-Handlers) (and writing one in .NET is made incredibly simple by using [SharpShell by Dave Kerr](https://github.com/dwmkerr/sharpshell)). Instead of writing one for .vsix, I wanted to make the default one, the one that handles zip files (known as Compressed Folders in Windows), treat .vsix as .zip archives. For this, I needed to assign zip's Drop Handler to .vsix. Since Drop Handlers are Shell Extensions based on COM, it must mean they have a GUID. And to list all Shell Extension GUIDs, we can use a nice little utility by [NirSoft](http://www.nirsoft.net/) called [ShellExView](http://www.nirsoft.net/utils/shexview.html).

Upon running ShellExView, we'll get a listing of all the Shell Extensions installed on our system. We know Windows has one for zipped files, pressing Ctrl-F and searching for *˜zip' takes us to to the **Compressed (zipped) Folder DropHandler**. We need the GUID for this handler, so double-clicking on the entry opens its Properties pane, where we can copy the GUID entry.

<img title="" style="border-top: 0px; border-right: 0px; background-image: none; border-bottom: 0px; padding-top: 0px; padding-left: 0px; border-left: 0px; display: inline; padding-right: 0px" border="0" alt="" src="http://i0.wp.com/hmemcpy.com/wp-content/uploads/2014/03/image1.png?resize=873%2C535" data-recalc-dims="1" />

Last step is adding this GUID as a valid Drop Handler for .vsix files. Steps to do this are described in the TL;DR above.

After restarting explorer.exe (or rebooting), we can now drag and drop files onto .vsix files!

<img title="" style="border-top: 0px; border-right: 0px; background-image: none; border-bottom: 0px; padding-top: 0px; padding-left: 0px; border-left: 0px; display: inline; padding-right: 0px" border="0" alt="" src="http://i2.wp.com/hmemcpy.com/wp-content/uploads/2014/03/image2.png?resize=790%2C359" data-recalc-dims="1" />

Happy hacking!
