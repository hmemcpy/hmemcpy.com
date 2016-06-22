---
title: 'Review: my new HP Spectre x360 2-in-1 convertible laptop'
date: 2015-12-04T16:38:45+00:00
---
<img style="float: right; padding: 5px;" src="{% asset_path image1.png %}" />I decided to get with the times, and get myself a mid-level ultraportable machine I can carry around while traveling. Knowing almost nothing about this category of computers (and having avoided touch-enabled hybrids/tables until now), I spent considerable time researching. My requirements were simple:

  * a secondary machine (my 3 year old behemoth HP EliteBook 8570w is still the best development machine I've got)
  * light, portable (so, about 13"), touch-enabled (most of them are, anyway)
  * good typing experience (I considered a Surface 3/4 with Type Cover keyboard, but typing experience got mixed reviews)
  * $1000 or less

<!-- more -->

I decided to take advantage of the Black Friday sales and finally settled on the [HP Spectre x360](http://store.hp.com/us/en/mdp/Laptops/spectre-x360-211501--1), a gorgeous 13" 2-in-1 convertible computer, which was designed by HP together with Microsoft, and given away at Build 2015 to the participants. I'm not going to review it here, I'll leave this task for Lisa Gade from [MobileTechReview](https://www.youtube.com/user/MobileTechReview), who did an exceptional job [reviewing every possible aspect](https://www.youtube.com/watch?v=I3Cn8IAxsoI) of this computer, including benchmarks. Lisa also did multiple follow-up reviews, comparing the Spectre to the [Surface Pro 3](https://www.youtube.com/watch?v=dp5lc1veQ6E), [Dell XPS 13](https://www.youtube.com/watch?v=5oCwB-T7Lr0), a [Macbook Pro](https://www.youtube.com/watch?v=byzl-gCu-c8) and even the new [Surface Book](https://www.youtube.com/watch?v=3DQxm6v6fGA). Needless to say, after watching all those reviews, I had no doubt the Spectre is going to be my new machine!

As I'm typing this, it turns out there's a [newer (limited edition) of the Spectre out](https://www.thurrott.com/windows/windows-10/6872/hp-spectre-x360-limited-edition-preview), with a 6th generation Skylake processor (mine was 5th generation Broadwell) and a gorgeous Ash Silver finish, but as I mentioned, I didn't need a spec'd out machine. My 5th gen i7 with 8GB of RAM and 256GB SSD suit me just fine, and I got no buyer's remorse! (/crying)

<img style="float: right; padding: 5px;" src="{% asset_path image2.png %}" />And now to some more interesting details. There were few things I needed to do, to make this machine _usable_. First, the keyboard backlight button. The Spectre x360 has a backlit keyboard which can be toggled on and off with the (Fn)F5 button, unfortunately, when it's off, the F5 button is still lit, reminding you to press it. Luckily, HP released a [BIOS update](http://support.hp.com/us-en/drivers/selfservice/HP-Spectre-x360-Convertible-PC-Series/7527520/model/7791778), adding an option to turn this light off. To access the BIOS, hammer on the Esc after powering the machine on, until you get a menu. Press F10 to enter the BIOS.

The second part had to do with repaving the machine and installing Windows 10 on it from scratch. Even though this is a Microsoft *signature edition* computer, meaning it comes with (very little) bundled software, I am old school (emphasis on the old), and wanted to repave and repartition the machine myself, from a bootable USB stick containing Windows 10. However, when I went to the drive selection in the post-boot menu, I did not see my USB stick &ndash; I could only see UEFI entries. A quick search led me to one of two possible solutions: enable Legacy Mode (CSM) in the BIOS, or [create a bootable UEFI Windows 10 USB stick](http://www.windowscentral.com/how-create-windows-10-usb-installation) using a wonderful utility called [Rufus](https://rufus.akeo.ie/), which not only supports creating bootable UEFI sticks, it's **x2 faster** than the old Windows USB utility! After creating the UEFI stick per instructions above, I was able to boot from it, and install Windows 10 from scratch.

I've now typed this review on the Spectre, and the experience is amazing! The keyboard feels sturdy, the trackpad is precise (albeit big &ndash; iPhone 6 big) and I even flipped the screen over to use some touch apps (for the first time ever). I am happy with my new HP Spectre x360 and can definitely recommend it!
