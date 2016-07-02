---
title: 'WinForms bug: NodeMouseDoubleClick event in TreeView will sometimes have the wrong node in EventArgs'
date: 2009-05-21T16:46:15+00:00
---
Here's a strange bug I've encountered today in a WinForms application. Usually, double clicking on a collapsed tree node (which obviously has child nodes) will expand it. Most of the time when we need something to happen when a child node is double clicked, but not the parent, we write something similar to:

<!-- more -->

```csharp
void NodeMouseDoubleClick(object sender, TreeNodeMouseClickEventArgs e)
{
    if (e.Node.Nodes.Count == 0)
    {
        // … handle child node
    }
}
```

To my surprise, I discovered today that by double clicking on a collapsed parent node, the `e.Node` parameter was not the node I actually double clicked on, but one of the child nodes. Since the sub-child nodes count was 0, the event handled the (incorrect) node.

I noticed that it was not the same node all the time &#8211; it was different. I made a small WinForms application with just a TreeView, and I filled it with the contents of my **C:\Windows** directory. I placed a `MessageBox.Show(e.Node.Text);` in the `NodeMouseDoubleClick` handler. And that helped me realize that the `e.Node` is actually the node that is currently under the mouse cursor!

Here's the initial state:
{% asset_img image17.png %}

Double clicking on **Fonts** makes the following happen:
{% asset_img image18.png %}

Notice where the cursor is &#8211; that's the node that was passed in the event handler. Apparently, during the expand, if there are more child nodes that fit on the screen, the parent node scrolls to the top, but the cursor stays in the same place where the double click occurred.

I googled up this problem and I found that this bug was [reported on Connect](http://connect.microsoft.com/VisualStudio/feedback/ViewFeedback.aspx?FeedbackID=304958), and it will be fixed in the next version.

In the mean time, the workaround is to use the TreeView's `SelectedNode` property instead.
