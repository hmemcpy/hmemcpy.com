---
title: 'The 2-minute PowerShell intro for someone who "hates PowerShell"'
date: 2014-12-10T14:06:25+00:00
---
Hi, I'm a developer, and I hate PowerShell<sup>*</sup>. For no reason in particular, PowerShell just never seemed that appealing for me as a developer, as it was always marketed towards sysadmins. And I never liked the syntax &ndash; all those dollar signs reminded me of PHP.

<!-- more -->

This recently changed, however. A client had a set of legacy perl scripts which nobody could maintain anymore &ndash; and I was tasked with rewriting them. Having recently spent some time writing a script for [Boxstarter](http://boxstarter.org/) &ndash; an amazing tool that allows you to automate software and environment installations of new machines, powered by [Chocolatey](https://chocolatey.org/), in PowerShell, I thought that it could be a good fit for the task. I knew the language is powerful enough to allow the creation of those very useful tools, so I decided to give it a shot. I was not disappointed!

Luckily, you already have all the tools you need to get started! Every Windows machine comes with both PowerShell and PowerShell ISE (Integrated Scripting Environment) already installed.

{% asset_img image.png "Figure 1: PowerShell ISE &ndash; an IDE for PowerShell with code completion (IntelliSense) and an integrated debugger." %}

Here's what you need to know about PowerShell:

You can do most of your development and debugging in the ISE &ndash; no need to type individual instructions in the PowerShell console. It's great as a REPL, but nothing beats an IDE. Tip: select a few lines in the ISE and press F8 &ndash; only those lines will be executed!

### What's so great about PowerShell?

**It's dynamic** &ndash; every variable can be treated as anything, but also support explicit typing (which are checked at runtime). Variables are prefixed with the `$` sign.

```ps
$my = "some string"
$my = 23
# Runtime error: Cannot convert value "23" to type "System.Xml.XmlDocument"
[xml]$myXml = $my 
```

**It's pipelined** &ndash; every variable or the output of every function can be piped as an input to another function using the pipe (`|`) operator. It's extremely useful when dealing with collections and other enumerable objects &ndash; allowing you to filter the elements and transform the result into whatever you need.

```ps
# a LINQ-like querying with pipelining. 
# The $_ is similar to C#'s lambda argument "x", e.g. Where(x => x.Name == "chrome") 
$ids = Get-Process | Where-Object {$_.Name -eq "chrome" } | Select-Object -Property ID 

# Where-Object and Select-Object can also be written "where" and "select": 
$ids = Get-Process | where {$_.Name -like "chrome" } | select -Property ID 
# "where" and "select" are aliases. Use Get-Alias to see all aliases in PowerShell.
```

**It supports everything you know from .NET &ndash;** although PowerShell defines its own idioms with regards to common operations, such as formatting strings for joining paths, you can use all objects from .NET to do the same thing.

```ps
$combined = Join-Path $rootDirectory "mySubdirectory" 
# can be written as: $combined = [System.IO.Path]::Combine($rootDirectory, "mySubdirectory")
```

**It's concise** &ndash; everything in PowerShell can be verbose or very concise. By leveraging aliases there are many ways to say what you mean. Here's an example: the following function gets a list of changed files between two SVN revisions, by executing the [svn diff](http://svnbook.red-bean.com/en/1.7/svn.ref.svn.c.diff.html) command, outputting the result as XML which looks like this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<diff>
<paths>
<path
   item="added"
   props="none"
   kind="file">hello.txt</path>
<path
   item="modified"
   props="none"
   kind="file">other.txt</path>   
</paths>
</diff>
```

This XML is stored into an `$output` object, which is defined as a .NET `XmlDocument`. The object is than being queried via XPath to get only items of kind *˜file' which are *˜modified'. Finally, only the text of the node is selected.

```ps
function Get-SvnDiff($fromRevision, $toRevision)
{
  [xml]$output = & svn diff -r $("{0}:{1}" -f $fromRevision, $toRevision) --summarize --xml
  $output.SelectNodes("/diff/paths/path[@item='modified' and @kind='file']") | % { $_."#text"}
}
```

Quite a lot is going on in this example, which demonstrate the Power of PowerShell:

  * A process is started with the `&` symbol. Can also be started with [Start-Process](http://technet.microsoft.com/en-us/library/hh849848.aspx) for more options.
  * Strings can be formatted with `-f`, however in this case they are a part of an expression, and have to be escaped into their own expression by using `$()`.
  * The `%` symbol is an alias of `foreach`, which is an alias of `ForEach-Object`. Use `Get-Alias -Definition ForEach-Object` to see all the alias definitions, or `Get-Alias %`, for example.
  * The last line in a function (or selection) is what gets returned (or printed out). In this case, the result of the last line is a single string, containing the value *˜other.txt' (it's the only modified file). If there was more than one result, the return would be an array.
  * Finally, to call this method, we use `Get-SvnDiff 1000 2000`, and we can use the pipe operator (`|`) to continue modifying the returned values.

And that's it! Sure, there is way more to know about PowerShell, but this should be more than enough to get started, or at least, not to get lost when reading and writing simple scripts.

Happy scripting!

<hr/>

<sup>*</sup>Well, slightly less now.
