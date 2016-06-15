---
title: Installing Windows 8 on HP EliteBook 8570w
date: 2012-09-30T11:37:29+00:00
---
<img style="float: right; padding: 5px;" width=200 src="http://www.www8-hp.com/in/en/images/8770w_hero_tcm_188_1453363.jpg" />I just got my brand new [HP EliteBook 8570w](http://www.hp.com/united-states/campaigns/workstations/8570w_features.html). I was looking for a new development machine for a while, and after long consideration decided on this custom build of the Ivy Bridge-based EliteBook. Here are the (important) specs:

<!-- more -->

  * HP EliteBook 8570w 15.6*
  * i7-3820QM
  * 16GB RAM 1600MHz DDR3
  * 256GB SSD + 512GB HDD (instead of optical drive)

Unfortunately, like many branded laptops, it came bundled with tons of*¦ software, which I preferred not having installed. That being said, I decided to finally give Windows 8 a try, and install it on this machine.

**DISCLAIMERS AND WARNINGS:** At the time of writing (Sept. 30, 2012), Windows 8 was not officially supported by HP. Modifying system partitions and installing unsupported Operating Systems and/or drivers might void your warranty! Proceed at your own risk!

The following is a recap of the steps I performed to upgrade my machine to Windows 8. Your configuration (and, therefore, experience) might be different.

## STEP 0 &ndash; PREPARATION

I have always preferred having two partitions, C: and D:, having all my source code, utilities, music and other things on the D: partition, so if I reformat my computer (which used to happen fairly often), I would keep all my data. Since I now had two physical drives, I decided to have the SSD as my primary (system) drive, and the HDD as the storage.

On HP machines, all the pre-installed software and drivers are located in the directory **swsetup**, located on the C: drive. I copied this directory to the D: drive. Next, I proceeded to **create an image** of the current system. HP machines come with a special partition that contain the recovery image (which restores the system to store-bought state). I usually _delete_ the recovery partition, since a) it takes 30GB off the primary storage (which in my case is an SSD, and 30GB is a lot of space for an SSD) and b) it defeats the purpose of the reinstall, since the preloaded software is still there.

## STEP 1 &ndash; INSTALLATION

After backing up the existing system, and copying the **swsetup** directory, I proceeded to install Windows 8. Since my new machine doesn't have an optical drive, I used the Windows USB Tool to create a bootable Windows 8 USB stick. I rebooted the machine, pressed Esc during the startup. In the boot menu, I selected F10 for boot order, and selected my USB drive.

In the setup, I selected Custom to make a clean install of the OS, then in the partition selection I **deleted** all the partitions from **Disk 0** &ndash; _System Reserved, HP Tools and HP Recovery_ partitions were all deleted, as well as the OS partition. What remained was the now-unallocated space of Disk 0 and the existing Disk 1 (which is the 2<sup>nd</sup> physical drive). I proceeded to select the unallocated space of Disk 0, and Windows 8 did the rest.

## STEP 3 &ndash; DRIVERS AND CONFIGURATION

After (surprisingly smooth) Windows 8 installation, I proceeded to go to the Device Manager. Compared to a clean Windows 7 install, almost every device driver was automatically installed by Windows 8.

First things I noticed that the trackpad was not working. Like many Windows laptops, HP too comes with the Synaptics tracpkad, and although the driver was seemed to be installed by Windows 8, the trackpad didn't register any mouse movements. I installed the drivers from **swsetup\Trackpad**, and the problem was solved!

N.B. The software and driver directories in swsetup are cryptically named. Fortunately, most of them contain a file with a .CVA extension. This is a plain-text file (you can open it with Notepad), it will tell you the complete software title (and description) of the files in the directory. You could use this information to rename the directories to something that makes more sense (I did).

![](http://i.imgur.com/yhR3osh.png)

Looking at the device manager, there are 4 unknown devices. I right-clicked on each of them, choosing Update Driver, and pointed the system to look at **swsetup** and its subdirectories. The setup quickly found the missing devices, all except one: an Unknown Device.

Double-clicking on the device revealed its ID, so a quick Google check revealed it was something called _Validity Sensors_, which turned out to be the fingerprint reader on my machine. There was a Validity Fingerprint Driver in the swsetup folder, and after installing it I didn't have any more yellow question marks!

## STEP 4 &ndash; MORE STUFF AND FINAL WORDS

Until HP releases Windows 8-compatible versions of their tools, I chose not to install the ProtectTools suite (for drive encryption/enhanced security log-on). I also didn't install any of the Intel and HP drivers, since Windows 8 picked most of them up. I did, however, install the **IDT HD Audio Driver**, for enhanced audio capabilities and the mute button support.

I expect HP to release Windows 8 compatible drivers soon, however it shouldn't stop you from upgrading to Windows 8 today!