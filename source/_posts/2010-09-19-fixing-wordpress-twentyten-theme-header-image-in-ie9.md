---
title: Fixing WordPress Twenty Ten Theme Header Image in IE9
date: 2010-09-19T16:23:50+00:00
---
**Update [Sep 27, 2010]:** A patch was accepted for this bug [[#14883](http://core.trac.wordpress.org/ticket/14883)], and it will be fixed in the next version of WordPress. **The fix below is considered obsolete, and provided only as reference.**

A friend let me know that in the new [IE9 beta](http://ie.microsoft.com/testdrive/) my blog doesn't look good. After a 35MB download, long install, and event longer reboot (!), I was finally able to see what he meant:

![](http://i1.wp.com/hmemcpy.com/wp-content/uploads/2010/09/image_thumb.png)

The header image shifted to the right, and this only happens in IE9. A quick search about the problem led me to [this question](http://wordpress.stackexchange.com/questions/1932/how-to-fix-the-ie9-wordpress-twenty-ten-header-image-display-problem) on the [WordPress StackExchange](http://wordpress.stackexchange.com/) site, where I learned that a ticket was opened for the WordPress team, and a workaround for the problem.

To fix this issue, go to the Admin dashboard of your WordPress, then under **Appearance** select **Editor**, and under **Styles** select **Stylesheet (style.css)**. Find the following piece of code:

```css
#branding img {
  border-top: 4px solid #000;
  border-bottom: 1px solid #000;
  clear: both;
  display: block;
}
```

Replace

    display: block;

With

    display: inline;

And press **Update File**. If you have any caching plug-ins, clear the cache.

**Update:** unfortunately, the fix above leaves a small white space between the image and the bottom access bar (as mentioned in the answer on StackExchange). To fix it, add the following directly below the `#branding img` block:

```css
#branding {
  line-height: 0;
}
```
