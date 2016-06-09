---
title: More fun with ReSharper annotations in ASP.NET MVC!
date: 2013-02-26T15:47:38+00:00
---
After my previous blog post on the subject, my good friend Avi Pinto asked if it was possible to *teach* ReSharper to treat an ASP.NET MVC `HtmlHelper` extension method to understand and navigate to relative paths within the project. I'm happy to report that not only this is possible, it also requires almost no effort at all!

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

<img style="background-image: none; padding-top: 0px; padding-left: 0px; display: inline; padding-right: 0px; border: 0px;" title="PathReferenceAttribute" alt="PathReferenceAttribute" src="http://i2.wp.com/hmemcpy.com/wp-content/uploads/2013/02/image1.png" width="414" height="135" align="right" border="0" />

In order to have ReSharper understand the string to be a real path reference, all we need to do is to decorate the `path` parameter of the extension method with a ReSharper [Code Annotation](http://www.jetbrains.com/resharper/webhelp/Code_Analysis__Annotations_in_Source_Code.html) attribute called **PathReferenceAttribute**. Our extension method will now look like this:

<pre class="brush: csharp; gutter: false">public static HtmlString RegisterVersionedScriptInclude(
    this HtmlHelper helper,
    [PathReference] string path)
{
    ...
}</pre>

After adding this attribute, ReSharper will now treat the string as a real path reference, providing us with all the goodness:

**Incorrect paths:**

<img style="background-image: none; padding-top: 0px; padding-left: 0px; display: inline; padding-right: 0px; border: 0px;" alt="" src="http://i2.wp.com/hmemcpy.com/wp-content/uploads/2013/02/image2.png?resize=900%2C60" border="0" data-recalc-dims="1" />

**Code completion:**

<img style="background-image: none; padding-top: 0px; padding-left: 0px; display: inline; padding-right: 0px; border-width: 0px;" title="" alt="" src="http://i0.wp.com/hmemcpy.com/wp-content/uploads/2013/02/image3.png?resize=416%2C272" border="0" data-recalc-dims="1" />

**Navigation** (by holding Ctrl-click, or Go to Declaration):

<img style="background-image: none; padding-top: 0px; padding-left: 0px; display: inline; padding-right: 0px; border-width: 0px;" title="" alt="" src="http://i0.wp.com/hmemcpy.com/wp-content/uploads/2013/02/image4.png?resize=461%2C45" border="0" data-recalc-dims="1" />

In addition, since ReSharper 6 the PathReferenceAttribute takes a basePath as a parameter, allowing you to specify the initial directory it will look in. So if we're always looking for scripts in, say, **Scripts** directory, we can specify it via

<pre class="brush: csharp; gutter: false">[PathReference("~/Scripts")]</pre>

and have our extension method look in **Scripts** first:

<img style="background-image: none; padding-top: 0px; padding-left: 0px; display: inline; padding-right: 0px; border-width: 0px;" title="" alt="" src="http://i1.wp.com/hmemcpy.com/wp-content/uploads/2013/02/image5.png?resize=481%2C272" border="0" data-recalc-dims="1" />

Supercharge your extension methods!
