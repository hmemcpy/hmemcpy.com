---
title: Adding a custom property page to existing project types in Visual Studio
date: 2015-03-27T22:53:18+00:00
---
_Note: this post assumes some knowledge developing Visual Studio Extensions (VSIX)._

Suppose you're developing custom tooling that enhances (or otherwise modifies) current project types (for example, C# class libraries or Web applications). This is most commonly done by specifying custom MSBuild properties, typically by adding a `.targets` file to the project file itself (possibly via NuGet, which can [import `.targets` files automatically](http://docs.nuget.org/Release-Notes/NuGet-2.5#automatic-import-of-msbuild-targets-and-props-files)).

One common way to interact with those custom properties is by adding a page in the project properties, however, most documentation about extending project properties refers to creating your own project systems. Any documentation about extending existing projects is either out of date, or nonexistent.

<!-- more -->

But, when there's a will &ndash; there's a way. TL;DR: Here's how to add a custom property page to a regular C# console application:

  1. Create an (empty) VSIX project 
  2. Add a reference to the following assemblies: `Microsoft.VisualStudio.AppDesigner.dll` (located in the GAC), and `Microsoft.VisualStudio.ManagedInterfaces.dll` (from the Visual Studio SDK) 
  3. Create a new class that derives from `Microsoft.VisualStudio.Editors.PropertyPages.PropPageBase` 
  4. Implement the class as follows:

```csharp
[ComVisible(true)]
[Guid("some-guid")]
[ProvideObject(typeof(MyPropertyPageProvider))]
public class MyPropertyPageProvider : PropPageBase
{
    protected override Type ControlType
    {
        get { return typeof(MyPropertyPageControl); }
    }

    protected override string Title
    { 
        get { return "My Property Page"; } 
    }

    protected override Control CreateControl()
    {
        return new MyPropertyPageControl();
    }
}
```

Make sure to provide a new GUID in the `GuidAttribute` (tip: if you use ReSharper, you can create new GUIDs on the fly by typing `nguid` and pressing Tab), we will need this GUID again soon. Specify the title of your property page, and provide an instance of a UserControl-derived (WinForms, baby!) page that will be the UI. Visual Studio provides an abstract `Microsoft.VisualStudio.Editors.PropertyPages.PropPageUserControlBase` class you can derive from.

**Important:** Visual Studio will try reading the size of the control from the assembly's compiled resources &ndash; this requires a .resx file for the user control. Best to create a new User Control using the Add &ndash; User Control context menu (so it can have a .Designer and a .resx files), and change the base type to `PropPageUserControlBase` afterwards.

One last piece of the puzzle is hooking it up &ndash; this is where a bit of MSBuild magic comes in. After running your extension (in the Experimental Instance), create a new, say, C# Console application. When the project is created, open its .csproj file in Notepad (or your favorite editor), and add the following property into one of the `PropertyGroup`s (or create your own `PropertyGroup`, e.g.):

```
<PropertyGroup>
  <CfgPropertyPagesGuidsAddCSharp>{some-guid}</CfgPropertyPagesGuidsAddCSharp>
</PropertyGroup>
```

Using the GUID from before. Save the .csproj file, and when you reload it in Visual Studio, you will now have a brand new (albeit empty) property page in the project's properties!

{% asset_img prop.png "Hello Property Page!" %}

(You can probably add this property dynamically with DTE from your extension, instead of modifying existing projects, but I haven't tried it.)

So what happened? Where did `CfgPropertyPagesGuidsAddCSharp` come from, and what makes it so special? Turns out, after a long investigation, it's an _undocumented_ property, which is a part of the legacy C# and VB project systems. When Visual Studio processes C# or VB projects, it will look for this property, and attempt to instantiate the COM class at a given GUID. If successful, it will add it as a property page.

I was able to confirm this works in Visual Studio 2013 and 2015, not sure about the earlier editions.

So there you have it, a bit of undocumented functionality makes the impossible possible :)

Happy hacking!
