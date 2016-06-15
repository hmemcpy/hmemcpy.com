---
title: Modifying Windows Live Writer blog content in PublishNotificationHook plugins' OnPrePublish
date: 2011-04-23T18:51:49+00:00
---
I'm writing a <a href="http://msdn.microsoft.com/en-us/library/ff747355.aspx" target="_blank">PublishNotificationHook</a> plugin for Windows Live Writer (don't worry, I will soon reveal what it is), and I noticed that there doesn't seem to be a way to control the contents (text or HTML) of the blog post in this type of plugin.

<!-- more -->

Further digging led me to understand that there used to be a method modify the contents via Reflection, as described by <a href="http://scottisafooldev.wordpress.com" target="_blank">ScottIsAFool</a>, Live Writer MVP and author of many great plugins, using his <a href="http://scottisafooldev.wordpress.com/2008/06/03/new-writer-plugins-using-the-new-sdk/" target="_blank">WriterUtils</a>, however this doesn't seem to work anymore with the latest version of Live Writer 2011.

I had discovered that on a Japanese blog called <a href="http://blog.sharplab.net/" target="_blank">SharpLab</a>, someone had posted <a href="http://blog.sharplab.net/computer/cprograming/windowslivewriter/433/" target="_blank">a way</a> to excavate an internal BlogManager object, which is used by Live Writer to edit the actual blog posts. The code needed a slight modification, but with the result I was able to modify the contents of my blog post!

I extracted this into an extension method, use this at your own risk!

<script src="https://gist.github.com/hmemcpy/938655.js" />