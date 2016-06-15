---
title: 'Boot to desktop in Windows 8: An in-depth analysis'
date: 2012-09-08T20:40:30+00:00
---
One of the most controversial decisions Microsoft made with regards to Windows 8 was the removal of the *classic* Start Menu, and replacing it with the new <strike>Metro</strike>Start screen. Furthermore, Microsoft made it impossible to go immediately to the desktop upon login in Windows 8 &ndash; it must be done via the new Start screen too.

<!-- more -->

I was told on twitter that the new Windows Server 2012 does boot into desktop by default. This made me very curious, and I decided to try and figure out the differences in the two operating systems myself. Below are my findings:

(Here's the **TL;DR** version: Windows Server 2012 indeed boots into desktop by default. Upon installing the *Desktop Experience* feature in Windows Server 2012, and after the subsequent reboot, it will no longer boot into desktop, but rather into the Start screen, just like Windows 8. However, there exists a registry key, which allows changing this behavior, and booting into desktop even with the Desktop Experience enabled.

On Windows 8, however, this registry key is not being read, so there is currently no way to _natively_ boot into desktop, without using some 3<sup>rd</sup> party software)

`/output:verbose`

Longer version: I decided to try and find out what happens during logon into Windows Server 2012, after a new install. I installed the trial version on a virtual machine, set a password for the Administrator account during setup. After the first login, I found myself in the desktop, and the Server Manager was launched automatically. I decided to turn off the automatic start in the settings.

My next step was to take a *snapshot* of all the file and registry activity that happens during the boot and logon. Armed with the perfect tool for the job &ndash; [Process Monitor](http://technet.microsoft.com/en-us/sysinternals/bb896645.aspx) by Sysinternals, I turned on **Enable Boot Logging**, located under Options, then rebooted Windows Server.
{% asset_img image1.png %}

After the reboot, I launched Process Monitor again, and was prompted to save the results of the boot logging into a PML file. I closed Process Monitor, and proceeded [installing the Desktop Experience](http://www.win2012workstation.com/desktop-experience/) in the Server Manager, but not before I took a VM snapshot of the current system state. The system needed to reboot, and once everything had finished installing, upon login I was presented with the new Start screen (having some new icons in it, mainly the Windows Store, and other *client* utilities.

Turning on boot logging again in Process Monitor I rebooted the system again, and after login saved the new results into another PML file. The new file was significantly larger than the previous, probably having to do with new files added to the system. I saved another system snapshot, and reverted to pre-Desktop Experience. What I wanted to do is to see the new files that were added/changed in the system. In order to do that, used the good *˜ol **dir /s** command to list all files in the Windows directory, and its subdirectories, piping the output to a text file. I did the same after reverting to the post-Desktop Experience snapshot. I then loaded the two text files into my favorite diff tool, [Beyond Compare](http://www.scootersoftware.com/moreinfo.php), and proceeded to carefully look at the differences.

Many files, having to do with *client* applications, were added to miscellaneous directories under Windows. There were additional references to something that is called **Immersive.UI**. I knew that sounded familiar, so I opened the two PML files side by side, and started looking for *Immersive*. After several identical results, I found a single difference between the two snapshots: a call by **explorer.exe** to a registry key called **ClientExperienceEnabled**, located at

<pre>HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Server</pre>

On the Desktop Experience snapshot it had the value 1, and on the pre-Desktop Experience it was 0. Using Process Monitor, I **Jumped To** the registry key, and tried setting it to 0. I was prompted that I did not have permission to change that value, even though I was an administrator on the system. I right-clicked on the parent key in Registry Editor, and selected **Permissions**. It turns out that the key's permissions were set to TrustedInstaller, meaning that the key can be only set by the operating system. I clicked **Advanced**, and changed the ownership to the Administrators group. Surprisingly, the system accepted the change, and I was then able to set the key's value to 0.

**After rebooting, when I logged in, I was back in the desktop, even with the Desktop Expreience enabled!**

Unfortunately, this trick does not work on Windows 8. Having done the same boot logging for Windows 8, I did not see any calls to the `ClientExperienceEnabled` key. Back in Windows Server, I wanted to know exactly who is responsible for calling that key. In Process Monitor, I double clicked on the line to bring up the **Event Properties** dialog, then went to the **Stack** tab.
{% asset_img image2.png %}

The Stack tab shows the call stack for the particular event, the pink <span style="color: #ff00ff;">**K**</span> specifies a kernel-mode calls, and the blue <span style="color: #0000ff;">**U**</span> specifies user-mode calls, which what I was looking for. It showed, that the calls to the registry were made by **twinui.dll**, a file that, turns out, exists in both Windows Server 2012 and Windows 8, however it's not being called in Windows 8.

At this point I'll skip the gory details and give you the bottom line: **twinui.dll** (and several others) checks for several things:

  * that we're running in a Windows Server (by calling the [GetSystemMetrics](http://msdn.microsoft.com/en-us/library/windows/desktop/ms724385.aspx) API)
  * that we are licensed for a feature called **explorer-ClientLoginExperienceAllowed** (by using the [SLGetWindowsInformationDWORD](http://msdn.microsoft.com/en-us/library/windows/desktop/aa965835.aspx) API, which is a part of the Windows [Software Licensing API](http://msdn.microsoft.com/en-us/library/windows/desktop/cc296101.aspx), responsible for querying the licensed system features<sup>[1]</sup>
  * that the registry key mentioned above exists, if the two conditions above are true

In conclusion, without modifying protected system files, or otherwise modifying the system to trick **twinui.dll** into thinking we're running on Windows Server, it's currently not possible to have Windows 8 boot into desktop. There are several [tricks](http://www.howtogeek.com/118106/go-directly-to-desktop-mode-in-windows-8-on-login-without-installing-extra-software/) and [utilities](http://retroui.com/) that force Windows 8 into desktop after login, but a *native* way is currently not possible.

* * *

<sup>[1]</sup> A few words on the Windows Licensing model: Windows stores system features in a registry key called [**ProductOptions**](http://technet.microsoft.com/en-us/library/cc727898.aspx), located in

<pre>HKLM\SYSTEM\CurrentControlSet\Control\ProductOptions</pre>

This key is protected by the operating system, and attempting to change its contents not only results in a Stop Error ([bug check code 0x9A](http://msdn.microsoft.com/en-us/library/windows/hardware/ff559317(v=vs.85).aspx)), it violates the Windows license agreement, disqualifying you from receiving Microsoft Support.

Some information about how to **_read_** the Product Options is available [here](http://www.remkoweijnen.nl/blog/2010/06/15/having-fun-with-windows-licensing/).
