---
title: 'Migrating from TFS to git to Visual Studio Online - the survival guide'
date: 2014-06-29T23:28:16+00:00
---
This is a step-by-step recount of my attempt to migrate an existing 3-year old TFS (TFVC) repository to git, while _keeping all the history_, and then moving it to [Visual Studio Online](http://www.visualstudio.com/), a TFS in the cloud. This wasn't an easy task, as there is no direct export-import built into either tools. I also ran into some problems during this lengthy process, and I describe the steps to solve them. Set aside a few hours of your time, brew some coffee (or tea), and let's get started!

<!-- more -->

# Step 1: TFS to git

We first need to export the entire TFS repository to git. This is achieved by *cloning* the entire TFS repository with [git-tfs](https://github.com/git-tfs/git-tfs) or [git-TF](https://gittf.codeplex.com/), both open source tools. While designed to do the same, mainly, providing a bridge between git and TFS, the former is an older, more mature project, and the latter is a tool created by Microsoft for the same purpose. I initially tried to use Microsoft's git-TF, but after more than **24 hours** of waiting for the clone to end, it **died with a Java exception** (the tool by Microsoft is written in Java).

First, install git-tfs. It's best installed with [Chocolatey](https://chocolatey.org/) by using `cinst gittfs`. Next, we need to get the exact name of the project we want to clone. Assuming your TFS server is https://tfs.contoso.com, first, run the following command to list all the branches:

```
git tfs list-remote-branches https://tfs.contoso.com/tfs/DefaultCollection
```

This will output all the branches that exist in the DefaultCollection. Branches marked with `[*]` are the root branches, and these are what we want to clone. Run the following command to clone the required branch, e.g.:

```
git tfs clone https://tfs.contoso.com/tfs/DefaultCollection $/Project/MyApp/Dev [<directory>]
```

This will clone the Dev branch (in this case) to a new directory specified in `[<directory>]`. If `[<directory>]` is not specified, a new directory called Dev will be created.

**The clone operation might take up to several hours**, depending on the size of your TFS repository. The cloning operation with git-tfs will pull each individual check-in, and will apply it as a series of git operations, _recreating the history_ exactly as it happened! Git-tfs will also run a git-gc operation every 100 commits, so the new repository size will be kept in check, and obsolete files will be removed.

After the clone operation is complete, you will have a git representation of the TFS repository on your local disk.

# Step 2: git to Visual Studio Online

After [setting up a free account](http://go.microsoft.com/fwlink/?LinkId=307137&clcid=0x409) in Visual Studio Online (VSO), we first need to create a new project, and make sure Git is selected as the source control. After the project had been created, we can go to the CODE tab, and be presented with instructions to either clone an empty repository, or push an existing one. We want to use the second option, so first, set the remote URL in our cloned git repository to point to VSO.

In a command prompt (or use any one of the 3<sup>rd</sup>-party visual Git clients), go to the cloned git directory and paste the first command, e.g.:

```
git remote add origin https://contoso.visualstudio.com/DefaultCollection/_git/MyProj
```

This will set the origin (the remote repository address) to point to our git repository in VSO.

The most important step is next: unfortunately VSO has a timeout limit of 1 hour for any connection, meaning that an attempt to push the entire repository might fail, if the repository is too big! What's worse, pushing is an atomic operation, it cannot be resumed in case of a timeout, you will have to start from the beginning.

Luckily, there's a workaround I was managed to find at the bottom of a [similar issue](http://social.msdn.microsoft.com/Forums/vstudio/en-US/bf7d7f99-ba50-48eb-bf0e-4fda818cf992/unable-to-push-a-git-repository) in MSDN forums. Basically, we can push our repository in smaller chunks, thus minimizing the chance of a timeout. This is not the ultimate solution, but it worked for me. Our problem is currently being able to push, subsequent cloning should be much faster, since download bandwidth is almost always faster than the upload.

Disclaimer: This is a somewhat advanced git usage, and I must admit, I don't quite understand it myself fully. Below is a series of commands I ran, based on the mentioned issue, and it worked in my case. YMMV. If you can explain this, please leave a comment below!

First, the issue tells us, we need to get an idea of the number of commits we have, by running the following:

```
git rev-list --all --count
```

In my case, the number was 4012, which I assume is the total number of commits.

Next, however, the issue says to run this:

```
git rev-list master --first-parent --count
```

Which is the *depth of the *˜first-parent' lineage of master*, according to the post author. Not quite sure what this meant (the documentation wasn't very helpful, either), running this command produced a number which was about half the previous one: 2512.

Not knowing exactly what the numbers meant, I decided to try and follow the post's advice, and split that number into 5 sections, of 500 commits each, and I pushed them in the following order:

```
git push origin master~2500:refs/heads/master
git push origin master~2000:refs/heads/master
git push origin master~1500:refs/heads/master
git push origin master~1000:refs/heads/master
git push origin master~500:refs/heads/master
```

And finally:

```
git push -u origin master
```

To push the remaining commits, and create a remote tracking branch for master. To make extra sure, I ran this last command again, and got *Everything up-to date* message.

Refreshing the CODE tab in VSO revealed that all my source code was uploaded successfully! I cloned the repository locally, and ran a diff between the two directories in Beyond Compare, just to make absolutely certain that everything was copied properly. It was!

# Step 3: VSO to FogBugz

Few more things left to migrate, and those are all the issues on FogBugz to VSO. In the meantime, though, we need to keep our source control integration with FogBugz. Turns out this is also not a simple task. But, this is a blog post for another day. Stay tuned!
