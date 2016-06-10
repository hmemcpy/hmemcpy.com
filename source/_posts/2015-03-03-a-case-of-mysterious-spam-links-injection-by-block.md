---
title: A case of mysterious spam links!
date: 2015-03-03T13:01:13+00:00
---
**Update:** _I was rightly corrected by the creator of uBlock, those are not links, but CSS selectors inside a `<style>` tag, to cause the offending links to be removed from the page. Furthermore, those particular rules are being fed from AdBlock Plus'_ [_EasyList_](https://easylist.adblockplus.org/en/)_, and they are not related to uBlock._

I was tweaking a [Jekyll](http://jekyllrb.com/) theme to match the style of our Bootstrap-based site, when I suddenly noticed an alarming links to porn/spam sites, visible inside Chrome tools:

<!-- more -->

{% asset_img image1.png %}

Alarmed, I didn't know what to make of this at first. It's a custom (paid) Bootstrap theme, so I suspected either the theme or one of its plugins was the culprit, however I could not find any code that seemed to inject this particular style.

Armed with fairly [little knowledge](/2014/03/how-nancy-made-net-web-development-fun/) of dealing with web development, I decided to try and set a breakpoint inside the Chrome tools on the text inside the `<style>` element itself, by right-clicking and selecting **Break on &ndash; Subtree modifications**:

{% asset_img image2.png %}

I reloaded the page and then found myself inside a script called **contentscript-start.js**, which turned out to belong to [uBlock Origin](https://chrome.google.com/webstore/detail/%C2%B5block/cjpalhdlnbpafiamejdnhcphjbkeiagm?hl=en):

{% asset_img image3.png %}

Thanks to George Pollard ([@porges](https://twitter.com/porges)) I was led to [this issue](https://github.com/gorhill/uBlock/issues/161) on the uBlock github, where it seemingly replaces all instances of `http://face*` with a matching filter (which, in this case, a link to a porn site). The reason for this is still unclear to me, as face* generates way more false positives (i.e. facebook).

This also explains the other link: the bottom of my Bootstrap page contains a link to the Facebook and LinkedIn pages. uBlock must be matching `http://link*` as well.

So if you find those while looking at your site through Chrome Dev Tools, don't be alarmed as I was &ndash; it's just your friendly neighborly adblock in action!
