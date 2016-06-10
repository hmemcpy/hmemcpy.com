---
title: 'Fixing a failed scheduled task: The operator or administrator has refused the request 0x800710E0'
date: 2012-10-04T11:10:26+00:00
---
I use the incredible [Everything](http://www.voidtools.com/) to find files on my computers. It's very fast and I have bound it to Win-Z (but not on Windows 8, more on that in another post) for easy access.

<!-- more -->

Unfortunately, the author of this tool did not sign it with a code-signing certificate, and upon log-on, a yellow UAC prompt always asks me if I want to run it.

As a workaround, there's a way to [start Everything as a Scheduled Task](http://www.voidtools.com/faq.php#How_do_I_bypass_the_UAC_to_run__Everything__with_administrative_privileges_on_system_startup) in Windows. However, the tutorial misses one important step &ndash; if your computer is not running on AC power, the task will fail to start with the error: **The operator or administrator has refused the request 0x800710E0**.

The solution is not immediately obvious, but it's an incredibly simple one &ndash; in the **Conditions** tab of the task's properties, simply uncheck the first option in Power:

![](http://i1.wp.com/hmemcpy.com/wp-content/uploads/2012/10/image2.png)

After pressing OK the task will start successfully!
