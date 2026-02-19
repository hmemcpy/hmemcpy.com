+++
title = "How to get changed files from SVN between two revisions with PowerShell"
date = 2014-12-16T13:38:07Z
+++
As part of [teaching myself PowerShell](/posts/the-2-minute-powershell-intro-for-someone-who-hates-powershell/) (and converting a legacy mess of perl scripts into something more manageable), I needed a way to export the files that were added or modified between two SVN revisions. After some searching, I came up with this PowerShell script: it takes a repository URL, a _from_ and _to_ revision numbers, and an output directory into which to export the files.

<!-- more -->

```powershell
function Export-SvnDiff($repo, $fromRevision, $toRevision, $outputDirectory)
{
    $xpath = "/diff/paths/path[@kind='file' and (@item='added' or @item='modified')]"

    [xml]$output = & svn diff -r $("{0}:{1}" -f $fromRevision, $toRevision) $repo --summarize --xml
    $output | Select-Xml -XPath $xpath | % { $_.node."#text" } | % { 
        $targetFile = Resolve-FullPath (Join-Path $outputDirectory ($_ -replace $repo))
        $targetDir = $targetFile | Split-Path
        New-Item -Force -ItemType directory -Path $targetDir | Out-Null
        & svn export -r $toRevision -q --force $_ $targetFile
        Write-Host ("$_ -> $targetFile")
    }
}
```

This script uses [`Resolve-FullPath`](https://github.com/michael-wolfenden/CodeCampServer/blob/master/scripts/Carbon/Path/Resolve-FullPath.ps1) cmdlet from the Carbon project. Turns out, PowerShell's own `Resolve-Path` doesn't work on files/paths that do not exist.

Here's how it works:

  1. It executes **[svn diff](http://svnbook.red-bean.com/en/1.7/svn.ref.svn.c.diff.html)** command with -**r** switch, which takes a range of revisions, e.g. 1000:1050. The **summarize** argument shows only the high-level information, and **xml** outputs the data as XML. 
  2. This XML is being queried with an XPath, extracting only the names of the items of kind *˜file' which were *˜added' or *˜modified'. 
  3. For every such file, its relative path is being taken by subtracting the repository path from the full filename. 
  4. The target (sub)directory for that file is being created, if it doesn't exist. 
  5. It then executes [**svn export**](http://svnbook.red-bean.com/en/1.7/svn.ref.svn.c.export.html) command on the current filename, limiting it to the _to_ revision, so that&nbsp; the changes are taken only until that revision. The file is written in the relative target directory.

This is probably far from *idiomatic* PowerShell, but it gets the job done! Your improvements are welcome, feel free to comment on the Gist!