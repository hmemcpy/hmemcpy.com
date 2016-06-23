---
title: 10 tips for making your technical presentation awesome!
date: 2012-10-05T16:07:46+00:00
---
I am, by no means, a [professional speaker](http://www.speakinghacks.com/). I am developer with passion for technology and learning, and being known for talking **_a lot_**, I sometimes speak at local user groups about particular topics. Here are some tips I've gathered for making my presentations a little bit better.

<!-- more -->

## 10. DON'T PANIC!

<img style="background-image: none; float: right; padding-top: 0px; padding-left: 0px; margin: 0px 0px 0px 5px; display: inline; padding-right: 0px; border-width: 0px;" title="" src="http://i2.wp.com/hmemcpy.com/wp-content/uploads/2012/10/image3.png?resize=244%2C154" alt="" align="right" border="0" data-recalc-dims="1" />There's an old Murphy's law, stating: *Anything that can go wrong, will go wrong*. Your computer might freeze, BSOD or reboot suddenly. The projector you're using might burn. Your code example might not compile due to the silliest thing (which you will miss due to pressure) &ndash; it's all OK!

The best way out of this situation is to remain calm, breathe normally, and try your best to recover from a bad situation. Keep talking about what you're about to do. If you're going to reboot &ndash; say it out loud, your audience will understand. The most important thing is to keep talking about what you're doing &ndash; as well as listening. If your audience is technical, they might yell out something you missed which will solve the problem. Which brings us to...

## 9. ALWAYS HAVE BACKUP

Always have backup of your entire presentation offline. I find it best to keep it in my [Dropbox](https://www.dropbox.com/referrals/NTIzMjM2NjE5?src=global9) folder, so that I could access it on any computer I, in case mine breaks down. Also, never rely on having steady internet connection. In conferences, the *free* WiFi tends to be overloaded, and you won't always be able to rely on your mobile phone's tethering. Make sure your entire demo runs without requiring an active internet connection.

## 8. CLEAN UP YOUR DESKTOP

[<img style="background-image: none; padding-top: 0px; padding-left: 0px; margin: 0px 0px 0px 5px; display: inline; padding-right: 0px; border: 0px;" src="http://i2.wp.com/www.stardock.com/products/fences/images/screenshots/fences_image.png?resize=244%2C184" alt="" align="right" border="0" data-recalc-dims="1" />](http://i2.wp.com/www.stardock.com/products/fences/images/screenshots/fences_image.png)Most of the time you will present on your own work/personal machine. It probably contains a bunch of icons that even you might not have used for a while &ndash; but nevertheless, they are there. Your audience doesn't have to see your *mess*. If you haven't already &ndash; install [Fences](http://www.stardock.com/products/fences/) &ndash; a free utility from Stardock that allows grouping your desktop icons into areas called &#8220;fences*. One of the most useful features of this little utility is the ability to **_hide_** all fences and icons with a double-click! All your icons will disappear out of view (unless you choose to keep them). This way you will have a desktop with just the things you need for your presentation.

## 7. LOWER YOUR RESOLUTION

As machines keep getting better and faster, so keeps their resolution growing higher. Unfortunately, human eyes and projectors have yet to catch up. When you connect your machine to the projector, it will typically lower your resolution. Depending on your projector's capabilities, best resolutions are 1280&#215;768, or if you have to, 1024&#215;768. Anything higher might not be visible to people sitting in the back.

## 6. RESET YOUR VISUAL STUDIO TO DEFAULTS

If you are using a non-default color scheme or font in your Visual Studio (or any other IDE), your audience might not going going to appreciate it as much as you do. Many developers never bother to change the defaults to suit their needs (some even still use <span style="font-family: 'Courier New';">Courier New</span>), and have hard time adjusting to non-standard settings and tools, such as dark backgrounds and productivity add-ins. However, instead of resetting your main theme for the sake of the presentation, here's a tip for creating a _new_ environment for Visual Studio:

  1. Open the Visual Studio Command Prompt (known as Developer Command Prompt in Visual Studio 2012)
  2. Type in the following: **devenv.exe /rootsuffix YourDemoName**

A new instance of Visual Studio will be launched, having a default set of settings (as if you just launched Visual Studio for the first time!). The **rootsuffix** switch tells Visual Studio to create an additional **_hive_**, copying the local disk and registry settings to another folder called **YourDemoName**. In this new instance, you can modify the settings of Visual Studio as you like (change fonts sizes, remove toolbars, turn off add-ins), and it won't affect your *normal* Visual Studio settings.

## 5. TURN OFF 3<sup>RD</sup> PARTY ADD-INS

This is a somewhat controversial topic. I heard people advocate that even when your audience is not familiar with tools like [ReSharper](http://www.jetbrains.com/resharper/), you should educate them while doing your presentation. I disagree. Unless this is a ReSharper presentation, or I know for a fact that my target audience all know the tool (or similar tools), I will disable it for the presentation, as I want to avoid surprising the audience. Every unfamiliar popup menu, window or dialog could cause the audience to get distracted and lose you! Make a habit of learning to use the default Visual Studio shortcuts.

[<img style="background-image: none; float: right; padding-top: 0px; padding-left: 0px; margin: 0px 0px 0px 5px; display: inline; padding-right: 0px; border-width: 0px;" title="Navigate To..." src="http://i1.wp.com/hmemcpy.com/wp-content/uploads/2012/10/SNAGHTML7b5e651_thumb.png?resize=244%2C176" alt="Navigate To..." align="right" border="0" data-recalc-dims="1" />](http://i1.wp.com/hmemcpy.com/wp-content/uploads/2012/10/SNAGHTML7b5e651.png)Did you know that since Visual Studio 2010 there's a Navigate To command? Press **Ctrl-,** (having reset your keyboard settings to default) and you'll be able to navigate to any file or member in your solution. Your audience might not know that either, so tell them! Tell them what you're about to do, which shortcut are you using. Same applies to the very useful **Ctrl-.** shortcut, which lets you import using declarations, generate method stubs and rename variables, all without having to use a 3<sup>rd</sup> party tool.

Another important tip is to **_use the mouse_** for almost everything! This might be the most controversial advice, but the people in the audience do not see your fingers! Unless you're continuously explaining what you're about to do, which file you're about to open or which operation you're about to perform, use the mouse to visualize that.

## 4. PRACTICE (AND REDUCE) YOUR DEMO

Even if you can't come up with a good demo in time for the presentation, just focus on the *killer features* of the topic of your presentation. It happened to me way too often that I wanted to show so much, but ended up talking about one particular feature that sparked interest. Less is always more in this case.

Make sure you know your demo by heart. Open Notepad (or your favorite note-taking application) and write down _every step_ of your demo, from creating a new project to adding a new class called *˜AwesomeDemo'. Keep this file open during your presentation, either on another monitor or even another computer (or a phone or a tablet). If you get stuck for any reason, look at it for what to do next.

## **3. KEEP TALKING**

<img style="float: right; margin: 0px 0px 0px 5px; display: inline;" title="" src="http://i2.wp.com/hmemcpy.com/wp-content/uploads/2012/10/image5.png?resize=160%2C160" alt="" align="right" data-recalc-dims="1" />Like I mentioned before, keep talking. Explain every step that you are doing or about to do. Nobody wants to listen to you breathe to your microphone, or being silent for a few minutes, while you type or look for some file. Sometimes, especially when something doesn't work, talking out loud about what's happening can help. It works for [Rubber duck debugging](http://en.wikipedia.org/wiki/Rubber_duck_debugging), it will work for your demo.

## **2. HAVE A RESET STRATEGY**

Have significant parts of your demo stored in an offline source control, such as Git. This will allow you to restore working state in case something goes wrong, and also prevent you from typing or using snippets &ndash; simply store changes as separate commits (or even separate branches), and reset to those commits or branches. This will allow you to go back and forward in time, without undoing/redoing any work.

## 1. HAVE FUN!

<img style="background-image: none; float: right; padding-top: 0px; padding-left: 0px; margin: 0px 0px 0px 5px; display: inline; padding-right: 0px; border: 0px;" title="" src="http://i0.wp.com/hmemcpy.com/wp-content/uploads/2012/10/image6.png?resize=244%2C184" alt="" align="right" border="0" data-recalc-dims="1" />This is perhaps the most important tip I have, as someone who is not a professional speaker &ndash; have fun! When you're nervous, your audience can tell, and **you're gonna have a bad time**. Don't panic if something goes wrong, or you're confronted with a question you don't have the answer to. Instead of imagining that the audience is naked, simply remember, that most of them would not want to switch places with you!

Good luck!
