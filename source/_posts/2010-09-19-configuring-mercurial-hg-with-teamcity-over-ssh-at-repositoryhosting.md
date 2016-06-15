---
title: Configuring Mercurial (Hg) with TeamCity over SSH at RepositoryHosting
date: 2010-09-19T11:30:00+00:00
---
At [Typemock](http://site.typemock.com/), we're making the change of moving our source control from SVN to Mercurial (Hg). Side note: **Hg** is a symbol for [Mercury](http://en.wikipedia.org/wiki/Mercury_(element) in the periodic table.

We use [TeamCity](http://www.jetbrains.com/teamcity/) as our continuous integration server, and it took some trickery to configure it to recognize the repository. For this, I will use a repository hosted at [RepositoryHosting](http://repositoryhosting.com/).

Here are the steps required for configuring Mercurial with SSH in TeamCity:

<!-- more -->

**Part 1:** Installing TortoiseHg and generating a cryptographic key-pair for secure authentication

  * Download and install [TortoiseHg](http://tortoisehg.bitbucket.org/). Make sure to install the correct version (32-bit or 64-bit).
  * Download and run [PuTTYGen](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) to generate a key for authentication.
  * Move the mouse over the panel to generate random seed used for key generation.
  * Copy the public key to clipboard, then go to your profile page e.g. `http://yournickname.repositoryhosting.com/users/my_profile`.
  * Go to **Public Keys**, click **New Key**
  * Paste the public key into the **Value** text field, then press **Add Key**, and afterwards **Save Changes**.
  * In PuTTYGen, click **Save Private Key**. You will be warned that your key is not passphrase protected. Press **Yes** to save the key _without a passphrase_.

**Part 2:** Configutre TeamCity to use Mercurial

  * Go to your Project and press **Edit Project Settings**.
  * Press **Create build configuration** and give it a name. Press **VCS settings** next.
  * Press **Create and attach new VCS root**, and give it a name as well (such as MyProject Mercurial).
  * Under **Type of VCS** choose **Mercurial**.
  * Under **HG command path** specify the full path to where TortoiseHg is located (e.g. `C:\Program Files (x86)\TortoiseHg`).
  * Under **Pull changes from** type in the URL of your hosting **without the username**, so that if your URL looks like this: 

  <pre>ssh://hg@mercirual.yourdomain.com/myproject/</pre>
    
  * omit the **hg@** from the URL, and only specify: 
    
  <pre>ssh://mercirual.yourdomain.com/myproject/</pre> 
    
  * Under **User name** type in **hg**. Leave the password blank. 
{% asset_img image1.png %}
    
**Part 3**: Modifying `Mercurial.ini`
    
  1. Go to where TortoiseHg is installed (e.g. C:Program Files (x86)TortoiseHg)
  2. Open the file **Mercurial.ini** in a text editor, and locate the **[ui]** section
  3. Add (or modify) the following line:
    
  <pre>ssh = "C:\Program Files (x86)\TortoiseHg\TortoisePlink.exe" -ssh -2 -i "c:\&lt;path to your key&gt;\privateKey.ppk"</pre>
    
  Press **Test Connection**. If TeamCity seems to hang at this point, and there are no message boxes appear on your screen (from a process called TortoisePlink.exe),
    
  1. Assuming TeamCity runs as a service, go to **services.msc**, find **TeamCity Web Server** and stop it.
  2. Go to **Properties**, then the **Log On** tab. and check the *Allow service to interact with desktop* checkbox.
  3. Restart the service.
    
When you've done that, the service will run as a console application, and you'll be able to see the output. Try testing the connection again. This time, if there were any errors, you'll be able to see them. Reverse this once you're done troubleshooting, or when you see the Test Successful message in TeamCity.
