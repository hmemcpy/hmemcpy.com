---
title: Enabling targeting MSTest projects to .NET 3.5 in Visual Studio 2010 SP1
date: 2010-12-11T13:45:48+00:00
---
Microsoft had just released [Visual Studio 2010 Service Pack 1 (beta)](http://www.microsoft.com/downloads/en/details.aspx?FamilyID=11ea69cb-cf12-4842-a3d7-b32a1e5642e2&displaylang=en), and one of its features is allowing re-targeting Test Projects to .NET Framework 3.5. Unfortunately, not without jumping through hoops; if you try re-targeting your test project to .NET Framework 3.5, you'll get this helpful message:

![](http://i2.wp.com/hmemcpy.com/wp-content/uploads/2010/12/SNAGHTMLb973eb.png)

The message text is not selectable, but [using this trick](/2009/02/awesome-tip-copy-text-from-any-messagebox-to-clipboard/) available in Windows, it's possible to copy the message text to clipboard, and from there copy the URL easily.

You will need to modify two config files in order to allow re-targeting. You will find the explanation in the [above URL](http://blogs.msdn.com/b/vstsqualitytools/archive/2010/12/09/additional-steps-for-enabling-re-targeting-of-net-framework-in-test-projects-in-vs-2010-sp1-beta.aspx).
