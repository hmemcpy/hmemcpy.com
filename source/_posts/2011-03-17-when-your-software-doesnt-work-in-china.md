---
title: When your software doesn't work in China
date: 2011-03-17T13:57:31+00:00
---
I had an interesting bug submitted by a user, he wrote that <a href="http://www.typemock.com" target="_blank">our product</a> was crashing in his Visual Studio 2010, which was a Traditional Chinese edition.

<a href="http://www.typemock.com/typemock-isolator-product3" target="_blank">Typemock Isolator</a>, being a Visual Studio add-in, adds a menu next to the Tools menu in Visual Studio. It does so by looking for an index of the *Tools* menu in the main menu bar, and simply adding the *Typemock* menu after it. However, the *Tools* menu is only called that in the English locale. In other languages, the menu might be called differently. In French, for instance, it's called *Outils*.

<!-- more -->

When creating a new Visual Studio 2008 Add-in (under Other Project Types &ndash; Extensibility), if selected the *Yes, create a Tools menu item* in page 4 of the wizard, the following code is generated in `OnConnect` method after completing the wizard:

```csharp
...
string resourceName;
ResourceManager resourceManager = new ResourceManager("MyAddin.CommandBar", Assembly.GetExecutingAssembly());
CultureInfo cultureInfo = new CultureInfo(_applicationObject.LocaleID);

if (cultureInfo.TwoLetterISOLanguageName == "zh")
{
    System.Globalization.CultureInfo parentCultureInfo = cultureInfo.Parent;
    resourceName = String.Concat(parentCultureInfo.Name, "Tools");
}
else
{
    resourceName = String.Concat(cultureInfo.TwoLetterISOLanguageName, "Tools");
}
toolsMenuName = resourceManager.GetString(resourceName);
...
```

Unfortunately, this auto-generated code violates almost every known good coding practice. In particular, it gives no clues as to why *zh* is different, and why it's handled separately.

Visual Studio menus are localized in the following way: a resource file, CommandBar.resx, is added to the project. This resource file contains translations of all common menus in Visual Studio, and each entry is defined by appending the <a href="http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes" target="_blank">two-letter ISO language code</a> to the menu name, so that the entry for *Debug* in Spanish, for example, is **esDebug**.

There are two separate entries for both Traditional and Simplified Chinese in the resource file, and the entries are prefixed with zh-CHS and zh-CHT (zh is a short for <a href="http://en.wiktionary.org/wiki/Zh%C5%8Dngw%C3%A9n" target="_blank">Zhōngwén</a>). Those identifiers refer to the old culture names. Since Windows Vista, the <a href="http://blogs.msdn.com/b/shawnste/archive/2007/12/13/zh-hans-zh-hant-and-the-old-zh-chs-zh-cht.aspx" target="_blank">new *zh-Hans* and *zh-Hant*</a> names are used, and the older names are kept for backwards compatibility. They can be found in the <a href="http://msdn.microsoft.com/en-us/library/system.globalization.cultureinfo.parent.aspx" target="_blank">Parent property</a> of the CultureInfo, specifying the current Visual Studio <a href="http://msdn.microsoft.com/en-us/library/0h88fahh.aspx" target="_blank">Locale ID (LCID)</a>.

Now that I had an understanding why *zh* was different, I was able to solve the bug by simply checking for the Chinese culture, and returning the correct identifier:

```csharp
private string GetCurrentLocaleName(CultureInfo cultureInfo)
{
    // Chinese (Traditional and Simplified) use "old" locale code,
    // zh-CHT and zh-CHS, which is the name of the parent culture
    if (cultureInfo.TwoLetterISOLanguageName == ChineseTwoLetterISOLanguageName)
    {
        return cultureInfo.Parent.Name;
    }

    return cultureInfo.TwoLetterISOLanguageName;
}
```
