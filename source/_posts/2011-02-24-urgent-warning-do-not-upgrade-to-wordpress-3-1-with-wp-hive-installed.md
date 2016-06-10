---
title: 'Urgent warning: Do not upgrade to WordPress 3.1 with WP-Hive installed'
date: 2011-02-24T23:52:45+00:00
---
**Update (03/03/2011):** WP Hive author had fixed the plugin, so now it's possible to upgrade to WordPress 3.1! Read all about it [here](/2011/03/wp-hive-now-works-with-wordpress-3-1/ "WP Hive now works with WordPress 3.1!").

As always, before upgrading WordPress _<span style="text-decoration: underline;">make a full backup of your installation and the database</span>!_

<!-- more -->

This is still being investigated, but it seems that having HP-Hive plugin for WordPress installed (even if deactivated), causes the following error upon upgrading to WordPress 3.1:

> **Fatal error**: Call to undefined function wp\_cache\_get() in **/public_html/blog/wp-includes/functions.php** on line **336**

A quick search led me to [this post](http://wordpress.org/support/topic/upgrade-to-31-wp_cache_get-issue) on the WordPress support forums, where people seem to suffer similar problem. The culprit seems to be [WP-Hive](http://wp-hive.com/), a plugin which allows running multiple WordPress blogs using a single installation.

After failing to find a proper solution to the problem, I reverted all my installation and database to version 3.0.5. I will update this post as soon as a fix available.
