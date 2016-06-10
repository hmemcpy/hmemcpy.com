---
title: Restoring Solution Platforms to Visual Studio toolbar
date: 2012-10-09T11:41:57+00:00
---
Every once in a while, for reasons unknown, the Solution Platforms combo box, which contains the AnyCPU, x86, etc. disappears. And every time when I need to restore it, I spend a good few minutes in the options. Here are the steps to bring it back:

<!-- more -->

  1. Right-click on the empty space between the toolbars in Visual Studio, select **Customize*¦** at the bottom
  2. In the Customize dialog, select the **Commands** tab
  3. Select **Toolbar**, then select **Standard** from the combo box. Scroll down until you find **Solution Configurations**, select it
  
    ![](http://i1.wp.com/hmemcpy.com/wp-content/uploads/2012/10/SNAGHTML4b85081.png)
  4. Press **Add Command**, in the new window select **Build** in Categories, then select **Solution Platforms** and press OK (or double-click)
  
    ![](http://i0.wp.com/hmemcpy.com/wp-content/uploads/2012/10/SNAGHTML4d1e5a1.png)

That's it! The next time this menu disappears, you will know where to find it.
