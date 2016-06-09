---
title: Permanently redirecting old blog post URLs to WordPress 3
date: 2010-09-17T16:52:04+00:00
---
I am in the process of migrating from SubText to WordPress, and one of the most important tasks on the checklist is keeping the old URLs alive. WordPress allows you to chose the URL format of the blog posts (Using **Settings &ndash; Permalinks**). I chose **Month and name** as my preferred style. SubText URLs also contain the post date and the **.aspx** suffix, as well as **archive** directory for some of the posts.

We first need to create a [regular expression](http://www.regular-expressions.info/) (or RegEx) to identify the old style URLs. An example of such URL is: `http://hmemcpy.com/archive/2010/06/07/turning-poor-man-performance-profiling-into-awesome-using-excel-pivot-tables.aspx`

I will be using RegexBuddy to help me create and test the regular expression, but you can use whatever free tool you like, such as [Expresso](http://www.ultrapico.com/Expresso.htm).

Let's identify the parts that are constant, and parts that we need to change:

  * Day is no longer needed, however we need to keep the year and the month: `2010` and `06`
  * Post title should be kept as is: `turning-poor-man-performance-profiling-into-awesome-using-excel-pivot-tables`
  * The suffix `.aspx` should be removed

Using RegEx, we need to create the following expression:

  * Keep `/blog/` and optionally match `archive` ([help](http://www.regular-expressions.info/optional.html))
<pre>/blog/(?:archive)/</pre>

  * Match the date, capturing year, month and date into numbered references ([help](http://www.regular-expressions.info/regexbuddy/dateyyyymmdd.html))
<pre>(19|20)dd[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])</pre>

  * Match the post title `turning-poor-man-performance-profiling-into-awesome-using-excel-pivot-tables` once ([help](http://www.regular-expressions.info/repeat.html))
<pre>(.*)?</pre>

  * Match `.aspx`, escaping the dot character ([help](http://www.regular-expressions.info/characters.html#special))
<pre>.aspx</pre>

And the combined expression:

```
/blog/(?:archive)/(19|20)dd[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])/(.*)?.aspx
```

All that is left now is install a WordPress plug-in called [Redirection](http://wordpress.org/extend/plugins/redirection/), and in its Settings page add a new redirection:

![](http://i0.wp.com/hmemcpy.com/wp-content/uploads/2010/09/SNAGHTML8075d84.png)

The **Target URL** value is combined with the numbered references (`$1` &ndash; year, `$2` &ndash; month and `$4` &ndash; post title). Make sure the **Regular expression** checkbox is checked.

C'est tout!
