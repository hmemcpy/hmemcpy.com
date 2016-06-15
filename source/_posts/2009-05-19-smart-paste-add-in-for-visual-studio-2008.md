---
title: Smart Paste Add-In for Visual Studio 2008
date: 2009-05-19T05:57:18+00:00
---
Say you need to paste a chunk of XML (or [WKT](http://en.wikipedia.org/wiki/Well-known_text)) into Visual Studio as a string literal (for your unit tests, or what not). How would you do it?

In C#, string literals can be represented in two ways:

<!-- more -->

{% blockquote MSDN http://msdn.microsoft.com/en-us/library/aa691090.aspx %}
C# supports two forms of string literals: regular string literals and verbatim string literals.

A regular string literal consists of zero or more characters enclosed in double quotes, as in `"hello"`, and may include both simple escape sequences (such as `\t` for the tab character) and hexadecimal and Unicode escape sequences.
 
A verbatim string literal consists of an `@` character followed by a double-quote character, zero or more characters, and a closing double-quote character. A simple example is `@"hello"`. In a verbatim string literal, the characters between the delimiters are interpreted verbatim, the only exception being a _quote-escape-sequence_. In particular, simple escape sequences and hexadecimal and Unicode escape sequences are not processed in verbatim string literals. A verbatim string literal may span multiple lines.
{% endblockquote %}

So when you have a chunk of text that looks like this: 

```php
PROJCS["OSGB 1936 / British National Grid",
    GEOGCS["OSGB 1936",
        DATUM["OSGB_1936",
            SPHEROID["Airy 1830",6377563.396,299.3249646,AUTHORITY["EPSG","7001"]],
            TOWGS84[375,-111,431,,,,],
            AUTHORITY["EPSG","6277"]],
        PRIMEM["Greenwich",,AUTHORITY["EPSG","8901"]],
        UNIT["DMSH",0.0174532925199433,AUTHORITY["EPSG","9108"]],
        AXIS["Lat",NORTH],
        AXIS["Long",EAST],
        AUTHORITY["EPSG","4277"]]
```

How would you go about turning this into an escaped string literal (verbatim or regular)?

Being as most programmers are, well, lazy, I didn't want to do yet another find/replace session. I googled for the first thing that came to mind, "Smart Paste Visual Studio 2008". I found this great add-in called [Smart Paster](http://weblogs.asp.net/alex_papadimoulis/archive/2004/05/25/141400.aspx) by Alex Papadimoulis (creator of [TheDailyWTF](http://thedailywtf.com)), which adds a highly configurable "Paste As..." context menu:
{% asset_img image.png %}

And now, all I need to do is "Paste As" string, to get this (with a few tweaks):

```csharp
"    PROJCS[\"OSGB 1936 / British National Grid\"," +
"        GEOGCS[\"OSGB 1936\"," +
"            DATUM[\"OSGB_1936\"," +
"                SPHEROID[\"Airy 1830\",6377563.396,299.3249646,AUTHORITY[\"EPSG\",\"7001\"]]," +
"                TOWGS84[375,-111,431,0,0,0,0]," +
"                AUTHORITY[\"EPSG\",\"6277\"]]," +
"            PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]]," +
"            UNIT[\"DMSH\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9108\"]]," +
"            AXIS[\"Lat\",NORTH]," +
"            AXIS[\"Long\",EAST]," +
"            AUTHORITY[\"EPSG\",\"4277\"]]"
```

Thanks for the Add-in, Alex!