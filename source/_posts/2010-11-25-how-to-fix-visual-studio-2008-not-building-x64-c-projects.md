---
title: How to fix Visual Studio 2008 not building x64 C++ projects
date: 2010-11-25T08:09:25+00:00
---
<img style="float: right; padding: 5px;" src="{% asset_path image1.png %}" />Something happened to my Visual Studio 2008 install, and I was no longer able to compile C++ projects in x64 configuration &ndash; the build would always skip it. The problem also manifested itself by showing an error message: **The operation could not be completed. Unspecified error** when I tried to view the C++ project properties in x64 configuration. I ran a repair installation of Visual Studio and [Service Pack 1](http://www.microsoft.com/downloads/en/details.aspx?FamilyId=FBEE1648-7106-44A7-9649-6D9F6D58056E&displaylang=en), it didn't help.

<!-- more -->

After many attempts to find the cause, I came up empty. I finally got a suggestion on twitter to try and install [Windows 7 SDK](http://www.microsoft.com/downloads/en/details.aspx?FamilyID=c17ba869-9671-4330-a63e-1fd44e0e2505&displaylang=en). It requires SP1 to be already installed, and installing it solved the problem! I was finally able to build and view properties of C++ projects in x64 configuration again!
