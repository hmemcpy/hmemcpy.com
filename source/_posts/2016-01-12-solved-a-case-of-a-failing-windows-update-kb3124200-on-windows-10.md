---
title: 'SOLVED: A case of a failing Windows Update (KB3124200) on Windows 10'
date: 2016-01-12T18:19:35+00:00
---
I'm writing this post mainly to myself, explaining how I figured out why this particular Windows Update package was failing to install on my Windows 10 (installation began, then rolled back). This can serve as a general troubleshooting step when google searches lead you nowhere.

<!-- more -->

{% blockquote TL;DR %}
 in my particualr case, (temporary) enabling the Administrator user (after running `sfc /scannow` in an elevated prompt, followed by `net user administrator /active:yes`) allowed the update to install successfully! After installing and rebooting the machine, I disabled the built-in Administrator account using `net user administrator /active:no` from an elevated prompt.
{% endblockquote %}

/verbose

After failing to install the update, from both Windows Update and manually downloading it, I turned to the web, trying to find solutions. Most of the forums describing the problem were either abandoned, or given the basic generic troubleshooting tips, which are rarely useful (all they tell you there's a problem, as if you didn't know).

One of those *tips* is running [sfc /scannow](https://support.microsoft.com/en-us/kb/929833). The result of running this check is a (sometimes huge) log file called CBS.log, located in 

    %WinDir%\Logs\CBS\CBS.log

This log file will also be created as part of the standard system file checking done by installing Windows Updates.

What I did was, after my computer failed to install, and rolled back the installation again, was open this log file in Notepad++, then searching for entries with **Error**. Surprisingly, I saw a few lines that looked like this:

```
2016-01-11 20:17:42, Info   CSI    00000046 Loading user account SID [l:92{46}]"S-1-5-21-3692211415-2751783221-3488552363-1001"
2016-01-11 20:17:42, Info   CSI    00000046 Loading user account SID [l:92{46}]"S-1-5-21-3692211415-2751783221-3488552363-500"
2016-01-11 20:17:42, Error  CSI    00000048@2016/1/11:20:17:42.338 (F) base\wcp\rtllib\inc\auto_hive.h(105): Error STATUS_OBJECT_PATH_NOT_FOUND originated in function Windows::Rtl::AutoHive::Load expression: (null) [gle=0x80004005]
...
```

So it seems that it was trying to load a user account with SID ending in `-500`, and failed. Googling for the error text led me to [this post](https://answers.microsoft.com/en-us/insider/forum/insider_wintp-insider_update/latest-kb3074665-update-fails-to-install/45f314d1-2ea8-452c-b59f-60440b9f4e46?page=3) on the Microsoft forums, describing a similar problem. A little down on page 3, someone suggested running a PowerShell command, dumping all the user SIDs to the console:

    get-wmiobject -class "win32_account" -namespace "root\cimv2" | sort caption | format-table caption, FullName, SID

Which led me to see that the problematic SID belonged to the Administrator user! On Windows 10 machines, the Administrator account is disabled by default, and this is why I suspected the update was trying to install itself into the Administrator user's hive, but couldn't find it.

{% asset_img powershell.png "Listing output in PowerShell" %}

I've enabled the Administrator account using a net user command:

    net user Administrator /active:yes

And tried installing the update again. To my surprise, it installed successfully and didn't roll back!

After rebooting, I verified the update was listed in Windows Updates' history, and disabled the Administrator account again.

If your updates failing to install:

  * run `sfc /scannow`
  * check CBS.log
  * hope for the best!

Good luck!
