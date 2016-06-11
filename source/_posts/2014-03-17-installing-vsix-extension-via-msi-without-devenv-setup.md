---
title: 'Installing a .vsix Extension via MSI without "devenv /setup"'
date: 2014-03-17T01:40:19+00:00
---
There are two ways to install Visual Studio extensions: via VSIX installed from the Visual Studio gallery (or by double-clicking, which executes VSIXInstaller.exe), or *manually*, by copying the files from a custom installer, typically MSI (and specifying a special `<InstalledByMsi>true</InstalledByMsi>` element in the `extension.vsixmanifest` file). The latter approach is generally used if the extension needs to perform additional tasks, such as running ngen or registering COM servers.

<!-- more -->

**TL;DR:** it is possible to register custom Visual Studio extensions by <a href="http://en.wikipedia.org/wiki/Touch_(Unix))">touching</a> (modifying the last accessed date) of the file `extensions.configurationchanged`, which is located in the 

```
%VSInstallDir%\Common7\IDE\Extensions
```

directory (in Visual Studio 2012 and above). This will cause Visual Studio to reload all the packages &ndash; in essence, this is equivalent of installing the package using VSIX from Visual Studio gallery. No devenv /setup required!

**Update:** a better way was found by [Julien Lebosquain](http://blog.lebosquain.net/), without requiring elevation at all! You can run

```
devenv /updateconfiguration
```

and it will cause Visual Studio to refresh its package cache on next restart.

* * *

The official Visual Studio guideline suggests that by using the MSI approach, the installer is required to run `devenv.exe /setup` after installation, to refresh Visual Studio package caches and settings, in order for the custom package to be installed. This approach, however, has several drawbacks and disadvantages to the VSIX installation.

The first and foremost &ndash; speed. Running `devenv.exe /setup` rebuilds the entire Visual Studio settings from scratch, which takes significant amount of time, depending on the machine. This could be improved by running the command with the `/nosetupvstemplates` switch, if the package you're installing does not install any templates.

The second issue is stability &ndash; running /setup on the user's machine may sometimes cause other extensions not to register correctly, and cause other extensions to fail to load. As a commercial product, this is obviously a problem, since this usually results in a support ticket, followed by an uninstall of your software (whether to attempt to repair the situation before reinstall, or worse, remove and never try your software again).

Failing to find an adequate solution, I [asked on StackOverflow](http://stackoverflow.com/questions/22300278/registering-an-unpacked-vsix-extension-via-msi-without-using-devenv-setup) about the possibility of migrating to a proper VSIX installation, with several limitations. In the end, after an extensive research of the problem, I discovered a solution which solved my immediate issue: VSIX installer, after unpacking the files into the target directory (it's a .zip file, after all), will touch a file located in the Extensions directory root, called `extensions.configurationchanged`. The next time Visual Studio restarts, if it detects a date change in this file, will re-register all the .pkgdef files it finds. This significantly reduces both the amount of time Visual Studio takes to load (by not rebuilding the entire configuration cache), as well as risk of breaking the environment.

Here's how to do it from WIX (courtesy of [Daniel Cazzulino](http://blogs.clariusconsulting.net/kzu/how-to-install-a-visual-studio-extension-with-templates-via-an-msi/)):

```xml
<CustomAction Id='VS2013TouchExtensions'
              Directory='VS2013_EXTENSIONS_DIR'
              Execute="deferred"
              Impersonate="no"
              ExeCommand='[SystemFolder]cmd.exe /c &quot;copy /b extensions.configurationchanged +,,&quot;'
              Return='ignore' />
```

(this executes the `copy /b filename +,,` command, which is the Windows equivalent of Unix `touch`)

This is an unofficial, unsupported scenario. But, this is what VSIX installer does, and I see no reason not to do this myself. Beware, and use at your own risk!
