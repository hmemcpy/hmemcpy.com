---
title: 'When good permissions gone bad - a case of a failed build'
date: 2014-06-09T16:08:08+00:00
---
I was called over to see if I could help solve a strange issue &ndash; every time the build script (Ant) for the client's Android app ran &ndash; certain files that were modified by the build script (a `.properties` file, few others), were suddenly inaccessible to other people logging to the machine &ndash; only the user who initiated the build could still write to the files. Looking at the file permissions tab proved as much: only the current user and the Administrators group could access the file!

<!-- more -->

My initial investigation into Ant's build.xml led me to an interesting discovery &ndash; all the files that lost their permissions were modified using the [ReplaceRegExp](http://ant.apache.org/manual/Tasks/replaceregexp.html) task for Ant &ndash; a task that could replace text in a file using regular expressions. Quick Google search for *replaceregexp ant file permissions* led me to [this similar issue](https://issues.apache.org/bugzilla/show_bug.cgi?id=36440), which was, unfortunately, closed as wontfix.


I decided to investigate for myself. Using my go-to tool for this task, [Process Monitor](http://technet.microsoft.com/en-us/sysinternals/bb896645.aspx), I decided to trace all activity of **java.exe** (which runs the Ant tasks), looking for anything that has to do with setting permissions or writing the file, filtering just the file I was interested in (**project.properties**). After running the specific Ant task that did a simple regex replace in the file, it was indeed changed, and its permissions were changed as well.

{% asset_img image1.png %}

However, looking at the File Summary window of Process Monitor (Tools &ndash; File Summary), I saw that not only there were no new ACL permissions set (Set ACL was called 0 times), no actual bytes were written!

{% asset_img image2.png %}

So how was it possible that the file was modified, but nothing was written? Looking back at the events in Process Monitor I also could not see any calls to WriteFile.

Feeling confused, I then started looking for anything that could appear relevant, until one entry in particular caught my eye: a call to **SetDispositionInformationFile** with a flag **Delete: True**.

{% asset_img image3.png %}

I checked who was calling this API from the Stack tab of this event's properties, and saw that it was a call to **deleteFile**, originating in **java.dll**. This confirmed my suspicion that the file was not written directly at all &ndash; but _replaced_ with another file, possibly from a temp directory.

My suspicions proved to be correct &ndash; looking at the [source code](http://svn.apache.org/repos/asf/ant/core/trunk/src/main/org/apache/tools/ant/taskdefs/optional/ReplaceRegExp.java) for ReplaceRegExp task I saw that it was exactly how it did it: by using

```java
FILE_UTILS.createTempFile("replace", ".txt", null, true, true);
```

to create a temporary file, and then later renaming that temporary file with the original file name!

`FILE_UTILS` turned out to be just a wrapper calling Java's [`File.createTempFile`](http://www.tutorialspoint.com/java/io/file_createtempfile_directory.htm). The 3<sup>rd</sup> argument, which was `null` in this case, tells `createTempFile` where to create the file. If `null` is passed, it will use the default `%TEMP%` environment variable.

Which ended up explaining the problem exactly &ndash; by default, it uses the local user's `%TEMP%` directory to create the temp file that replaces the original one. The default per-user `%TEMP%` directory located in the `%LOCALAPPDATA%` directory of the user's profile &ndash; meaning only the current user (and local Administrators) can access it! This means, that any file created in this directory will inherit the same permissions! In our case, ReplaceRegExp's implementation caused the per-user temp file to overwrite the file that was in a public folder, causing it to lose all permissions!

A quick workaround for the problem was to set the TEMP directory to `c:\temp`, temporarily, during the build.

Next time your Ant script causes issues with file permissions &ndash; make sure your files are not replaced under your nose.
