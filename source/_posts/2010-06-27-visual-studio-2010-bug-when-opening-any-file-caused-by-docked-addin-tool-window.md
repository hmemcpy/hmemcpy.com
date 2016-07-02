---
title: 'Visual Studio 2010 bug: NullReferenceException when opening any file, caused by a docked add-in tool window'
date: 2010-06-27T07:04:44+00:00
---
Here's an issue I've been struggling with: it seems that by accessing a certain property of a _docked_ tool window of an add-in, an exception is thrown somewhere inside Visual Studio 2010. It's caught internally, and the exception message, *Object reference is not set to an instance of an object*, is shown whenever I was trying to open any file (code or otherwise).

<!-- more -->

Here's the offending code (this **OnConnection** method belongs to a C# Add-in code, it's pre-generated when you create a new Add-in for Visual Studio):

```csharp
public void OnConnection(object application, ext_ConnectMode connectMode, object addInInst, ref Array custom)
{
  _applicationObject = (DTE2)application;
  _addInInstance = (AddIn)addInInst;

  const string guidString = "{7CAB9543-0A69-4971-B154-01BC2DAAE2ED}"

  object dummy = null;
  var windows = (Windows2)_applicationObject.Windows;
  var buggyWindow = windows.CreateToolWindow2(_addInInstance, Assembly.GetExecutingAssembly().Location, typeof(WindowControl).FullName, "Buggy", guidString, ref dummy);

  buggyWindow.Visible = true;

  if (buggyWindow.LinkedWindowFrame.LinkedWindows.Count == 1)
  {
    // does not matter what happens here.
  }
}
``` 

It seems that accessing the window's **LinkedWindowFrame.LinkedWindows** property causes a corruption when the add-in is docked, which will manifest itself upon attempting to open a file.

I submitted this issue to [Connect](https://connect.microsoft.com/VisualStudio/feedback/details/554999/object-reference-is-not-set-to-an-instance-of-an-object-appears-when-opening-any-file-in-solution-caused-by-a-docked-add-in-tool-window), including steps to reproduce.

**Update:** It seems that the issue was fixed! Microsoft will include the fix in the next Visual Studio 2010 update!

