---
title: Installing Ubuntu in Windows Virtual PC
date: 2011-02-16T11:20:46+00:00
---
I was trying to install Ubuntu using [this tutorial](http://www.hanselman.com/blog/InstallingUbuntu104LTSOnWindowsVirtualPCOnWindows7.aspx) by Scott Hanselman, where upon pressing *Create virtual machine*, I was met with the following error message:
<!-- more -->
{% asset_img image.png %}

I couldn't immediately find the option in the BIOS, so I wrote down the BIOS Version (which was TYG4110H.86A), and later downloaded a BIOS upgrade from the Intel site.

Mine was an Intel DG41TY motherboard, and the option I was looking for was under **Security &ndash; IntelÂ® VT**. I set it to [Enabled], saved and quit the BIOS. Upon returning to Windows I got a *Not Genuine* prompt, which luckily went away on the next reboot. Afterwards I was able to create a new virtual machine, and was able to follow Scott Hanselman's <a href="http://www.hanselman.com/blog/InstallingUbuntu104LTSOnWindowsVirtualPCOnWindows7.aspx" target="_blank">guide</a> to install Ubuntu.
