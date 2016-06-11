---
title: 'How to enable login verifications on Twitter from "unsuppored" countries'
date: 2014-04-26T17:35:45+00:00
---
It's funny how a random twitter rant can yield valid solutions. One such rant between [@omervk](https://twitter.com/omervk) (who co-runs [plaintextoffenders.com](http://plaintextoffenders.com)) and myself regarding enabling Two Factor Authentication (2FA, or *login verification*) on twitter being unavailable for people in Israel, caught the attention of [Per Thorsheim](https://twitter.com/thorsheim), an independent security consultant and founder of the [Passwords conference](http://passwordscon.org/). Per, turns out, was interested in this problem because of another matter, that Twitter seemingly _turned off_ login verification for people who do not have their phone numbers associated with Twitter! Per wrote about his own experiences trying to enable 2FA on twitter [here](http://securitynirvana.blogspot.no/2014/04/did-twitter-silently-remove-login.html).

<!-- more -->

So what is the problem exactly? In order to enable login verifications on Twitter, turns out, you need to _either_ associate your mobile phone number with twitter, or enable sending login verifications to your iOS or Android twitter app. The latter, turns out _also_ requires your phone number!

Here's how it supposed to work: you go to the [**Security and privacy**](https://twitter.com/settings/security) settings in your twitter account. If no phone number is associated, you will see these options:

{% asset_img image1.png %}

Notice that both *Send* options are disabled. Pressing the **add a phone** link takes you to a page where you can enter your phone number (after selecting your country and carrier), however in my case, I got this message after submitting:

{% asset_img image2.png %}

OK, so I can't add a phone number on the twitter website. Let's try enabling login verifications on my (Android) twitter app. Go to Settings, your twitter username, then press Security:

{% asset_img image3.png %}

What! I am _still_ being asked to add a phone number!

This is the part where I initially gave up, but it turned out that clicking **Add phone** takes you to the mobile twitter page (in your phone's browser), where you can enter your phone number, and in my case **twitter accepted it, and sent me a verification SMS**!

The UX is confusing at this point, after adding my number, I got an SMS with a 6 digit verification code (and short t.co URL to continue verification), but no place in the page to enter it! In fact, I was asked to **remove** the phone number at this point:

{% asset_img phone1.png %}
{% asset_img phone2.png %}

Very odd. However, pressing the **manage** link above (in the yellow bar) took me to the actual verification page where I was asked to enter the code from the SMS message:

{% asset_img image5.png %}

And after pressing Verify, I got a message confirming that my phone number was successfully added!

{% asset_img image6.png %}

At this point, after going back to the Security and privacy settings on twitter, I saw that my phone number was now added, and could turn on login verifications!

{% asset_img image7.png %}

Also, going to the Security settings on my Android twitter app were now also working!

In conclusion, the steps above may work for you, even if you can't add your phone number on the twitter website. Did it work for you? Please leave a comment with your country/carrier, and any additional information!

Good luck, stay secure!
