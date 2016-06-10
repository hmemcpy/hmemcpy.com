---
title: Upgrading TortoiseHg to v2.0
date: 2011-03-07T12:16:50+00:00
---
Version 2.0 of <a href="http://tortoisehg.bitbucket.org/" target="_blank">TortoiseHg</a>, the best Windows client for the <a href="http://mercurial.selenic.com/" target="_blank">Mercurial</a> distributed source control system, was released a few days ago, featuring a complete UI overhaul and numerous fixes and improvements.

<!-- more -->

One change in particular should be noted for users on 64-bit Windows &ndash; the default installation directory had changed from **C:Program Files (x86)** to the 64-bit **C:Program Files**, and some files were moved into subdirectories.

If you're using SSH, and after upgrading you are getting the following message when trying to perform remote operations, such as **hg pull**:

<pre>remote: The system cannot find the path specified.
abort: no suitable response from remote hg!</pre>

In your **mercurial.ini** (typically found in **C:\Users\<username>**), make sure to set the correct path to **TortoisePlink.exe**, such as:

<pre>ssh="C:\Program Files\TortoiseHg\bin\TortoisePlink.exe" -ssh -i "C:\private.ppk"</pre>
