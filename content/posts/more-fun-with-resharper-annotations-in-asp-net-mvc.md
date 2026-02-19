+++
title = "More fun with ReSharper annotations in ASP.NET MVC!"
date = 2013-02-26T15:47:38Z
+++
After my previous blog post on the subject, my good friend Avi Pinto asked if it was possible to *teach* ReSharper to treat an ASP.NET MVC `HtmlHelper` extension method to understand and navigate to relative paths within the project. I'm happy to report that not only this is possible, it also requires almost no effort at all!

<!-- more -->

Considering the following extension method:

```csharp
public static HtmlString RegisterVersionedScriptInclude(
    this HtmlHelper helper,
    string path)
{
    ...
}
```

which is used in the following way:

```csharp
<%= @Html.RegisterVersionedScriptInclude("/Scripts/jquery.ellipsis.js") %>
```

In order to have ReSharper understand the string to be a real path reference, all we need to do is to decorate the `path` parameter of the extension method with a ReSharper [Code Annotation](http://www.jetbrains.com/resharper/webhelp/Code_Analysis__Annotations_in_Source_Code.html) attribute called **PathReferenceAttribute**. Our extension method will now look like this:

```csharp
public static HtmlString RegisterVersionedScriptInclude(
    this HtmlHelper helper,
    [PathReference] string path)
{
    ...
}
```

After adding this attribute, ReSharper will now treat the string as a real path reference, providing us with all the goodness:

**Incorrect paths:**
{{ image(path="image1.png") }}

**Code completion:**
{{ image(path="image2.png") }}

**Navigation** (by holding Ctrl-click, or Go to Declaration):
{{ image(path="image3.png") }}

In addition, since ReSharper 6 the PathReferenceAttribute takes a basePath as a parameter, allowing you to specify the initial directory it will look in. So if we're always looking for scripts in, say, **Scripts** directory, we can specify it via

```csharp
[PathReference("~/Scripts")]
```

and have our extension method look in **Scripts** first:
{{ image(path="image4.png") }}

Supercharge your extension methods!