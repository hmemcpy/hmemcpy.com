---
title: Preventing a certain Windows Update from installing on Windows 10
date: 2015-04-15T15:30:26+00:00
---
This post explains how to prevent a certain update from installing on a Windows 10 machine (at the time of writing, build 10049). The information below might not be accurate/relevant for future updates.

<!-- more -->

**UPDATE:** Microsoft has released a [tool to hide unwanted updates](https://support.microsoft.com/en-us/kb/3073930), which makes the process described below much simpler:

{% asset_img image.png "Show or hide updates" %}

<hr/>
During its preview, Windows 10 does not allow (by default), changing how updates are installed. It was possible to modify this using various [Group Policy settings and a bit of registry tweaking](http://www.askvg.com/how-to-change-windows-update-settings-when-managed-or-disabled-by-system-administrator/), but since build 10049 it no longer works &ndash; it's not possible to restore the *old* Windows Update applet in Control Panel.

On my machine (HP EliteBook 8570w), an update for the Synaptics TouchPad drivers took away my middle button, it simply did not appear anymore on the TouchPad properties. Uninstalling the update, and installing the Windows 8.1 Synaptics driver from the HP website helped, but within a day it was automatically updated again.

An answer on SuperUser suggested [disabling all automatic driver updates](http://superuser.com/a/665163/101), but I didn't want to do that. Luckily, I found a way to disable this particular update despite Windows Update settings were not changeable with a wonderful set of PowerShell tools called [Windows Update PowerShell Module](https://gallery.technet.microsoft.com/scriptcenter/2d191bcd-3308-4edd-9de2-88dff796b0bc).

Here's how to install the PowerShell module and disable unwanted Windows Updates:

  * Download the [Windows Update PowerShell Module](https://gallery.technet.microsoft.com/scriptcenter/2d191bcd-3308-4edd-9de2-88dff796b0bc), and extract it to either

```
%USERPROFILE%\Documents\WindowsPowerShell\Modules
```

or

```
%WINDIR%\System32\WindowsPowerShell\v1.0\Modules
```

(the former does not require elevation)

  * Temporary disable Execution Policy, to allow importing unsigned scripts. From an elevated PowerShell console type:

```
Set-ExecutionPolicy Unrestricted
```

followed by:

```
Import-Module PSWindowsUpdate
```

After the module had been imported, restore the Execution Policy to a reasonable setting, such as `RemoteSigned`.

  * Uninstall the unwanted update (if installed), then run the following command to get a list of all available windows updates:

```
PS> Get-WUList

ComputerName Status KB          Size Title
------------ ------ --          ---- -----
LAMBDACORE   D-----            65 MB Synaptics driver update for Synaptics SMBus TouchPad
LAMBDACORE   D----- KB2956185  68 MB Update for Microsoft OneDrive for Business (KB2956185) 64-Bit Edition
LAMBDACORE   D----- KB2965255  11 MB Update for Microsoft Office 2013 (KB2965255) 64-Bit Edition
...
```

  * Hide the *Synaptics driver update* by issuing the following command:

```
PS> Hide-WUUpdate -Title "Synaptics driver*"

ComputerName Status KB          Size Title
------------ ------ --          ---- -----
LAMBDACORE   D--H--            65 MB Synaptics driver update for Synaptics SMBus TouchPad
```

The letter H now signifying that the update is hidden! That's it, the update will now be hidden from Windows Updates, and won't be installed. To unhide, run:

```
PS> Hide-WUUpdate -Title "Synaptics driver*" -HideStatus:$false
```

Now, all I have to do is [change the two-finger scroll direction](/2013/12/how-to-change-two-finger-scroll-direction-in-synaptics-touchpad/), and I can get back to work!
