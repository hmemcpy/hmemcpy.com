---
title: How to convert Subversion repository to Mercurial (Hg) - it's easier than you think!
date: 2010-11-26T14:51:35+00:00
---
Converting SVN to Mercurial, while keeping all the commit history, might sound like a hard thing to do, but in fact it isn't! This functionality is already built into Mercurial, it's just not enabled by default.

<!-- more -->

I will be using [BitBucket](http://bitbucket.org/) as the Mercurial repository host for this example. You will also need the latest version of [TortoiseHg](http://tortoisehg.bitbucket.org/).

Conversion is done using the command `hg convert`, however the Convert extension is not enabled by default. To enable it, locate the file `Mercurial.ini`, typically located in your` %UserProfile%` drectory (`C:\Users\<username>`) in Windows 7). Open it in Notepad, and locate the following section:

    [extensions]

Add it, if it doesn't exist. Directly below the section name add the following line:

    hgext.convert= 

Save the file, and open a command prompt. Type <`hg convert`, and if the output shows usage for the convert options, it means that the extension was enabled successfully.

To begin converting, simply type:

    hg convert C:\code\YourProject

Where `YourProject` is the SVN root of your project. Mercurial will create a new directory, appending the suffix &ndash;**hg** (e.g. YourProject-hg), and will use it as a destination. Please note that this may take a long time, depending on the size of your SVN repository.

If you'd like to convert a specific branch, or a specific revision, you can specify [additional options](http://mercurial.selenic.com/wiki/ConvertExtension) to the command.

Once the process is completed, navigate to the destination directory, and use `hg push` to push all the changes to the repository:

<pre>hg push http://bitbucket.org/&lt;username&gt;/YourProject</pre>

That's it!
