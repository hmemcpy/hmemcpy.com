---
title: Silly (but serious) UI bug in GoToMeeting's Schedule dialog and Hebrew locale
date: 2011-01-11T12:01:17+00:00
---
At [Typemock](http://www.typemock.com/) we use [GoToMeeting](http://www.gotomeeting.com/) to conduct [webinars](http://www.typemock.com/webinars) and do online customer support sessions. When I tried to schedule a meeting with a customer the other day I encountered the following problem:

<!-- more -->

Typically, when clicking the Schedule a Meeting button (either via the context menu or the Outlook add-in), the next suggested Start time is at the start of the next hour, so that if it's currently 13:23, the suggested Start time should be 14:00, and End time 15:00. When your system's regional settings are set to Hebrew, upon opening the schedule dialog, the times are shown like this:

![](http://i2.wp.com/hmemcpy.com/wp-content/uploads/2011/01/image2.png)

From the first glance it would seem that GoToMeeting suggests to schedule the meeting at 14 minutes past midnight, with duration of 1 minute. In fact, the displayed times are flipped, showing the minutes first.

I reported this bug to GoToMeeting. Until it's fixed, if you're using Hebrew regional settings (or perhaps other RTL language), make sure you enter the time correctly, that is either type 00:15 to schedule at 15:00, or change your locale to English.
