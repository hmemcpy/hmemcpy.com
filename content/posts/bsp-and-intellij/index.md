+++
title = "Using BSP effectively in IntelliJ and Scala"
date = 2021-09-20T09:54:44Z
+++
I've been using the BSP support in IntelliJ for over 6 months now, and while the experience wasn't always smooth, it's definitely worth considering switching to BSP over sbt. I've recently contributed a couple of fixes to sbt's implementation of BSP, adding a few missing pieces, allowing improved support in IntelliJ using sbt's native BSP server. I am grateful to sbt maintainer [Adrien Piquerez](https://github.com/adpi2) of Scala Center and [Justin Kaeser](https://github.com/jastice) of JetBrains, who implemented the BSP support in IntelliJ for their hard work and great help!

This post is a step-by-step tutorial on how to use and get the most out of the BSP support in IntelliJ.

<!-- more -->

### Background

BSP, or the [Build Server Protocol](https://build-server-protocol.github.io/), is a specification for abstracting over build tools, designed in collaboration between JetBrains and the Scala Center. It derives from LSP (Language Server Protocol), a [Microsoft specification](https://microsoft.github.io/language-server-protocol/) for building rich editor tooling for various programming languages, such as Scala (via [Metals](https://scalameta.org/metals/)) or Haskell (via [haskell-lsp](https://github.com/haskell/lsp)).

The BSP makes the job of integrating build tooling into IDEs easier. Traditionally, the editor would have to execute the build tool (e.g. sbt or mvn) as an external process, read its output, and render the result accordingly. By exposing a common protocol, the IDE (the BSP client) can speak to the build tool (the BSP server) directly, resulting in much faster and more fine-grained incremental compilation, as well as receiving the output payload back via the protocol. For more information, I recommend [this blog post](https://blog.jetbrains.com/scala/2019/08/08/integrating-developer-experiences-the-build-server-protocol-in-the-intellij-scala-plugin/) from Justin Kaeser of the Scala plugin team at JetBrains. 

The major benefit of using BSP instead of importing the sbt project directly is the fact that the server will *run constantly in the background*, allowing IntelliJ to communicate via the protocol instead of launching external processes. In addition, the **build on save** feature enables a much faster feedback whether your code really compiles, especially since IntelliJ may sometimes incorrectly mark perfectly compiling code with red squigglies or other types of errors. Finally, build tools other than sbt may implement the BSP protocol, and will be available to use in IntelliJ without having to add custom support.

### Support in sbt

Prior to sbt 1.4, BSP support in Scala was only available via a tool called [bloop](https://scalacenter.github.io/bloop/) - a client and a server that implements the BSP protocol. As of version 1.4, sbt [natively supports BSP](https://www.scala-lang.org/blog/2020/10/27/bsp-in-sbt.html) which technically makes bloop no longer required, however some outstanding issues in sbt were only [fixed in the recent versions](https://eed3si9n.com/sbt-1.6.0-beta) (1.6.0-M1 at the time of writing).

IntelliJ supports BSP using *both* bloop and sbt, however there are slight differences between them. In particular, IntelliJ will fail to highlight and provide code completion (or detect changes) in the `build.sbt` file imported with bloop due to some missing functionality that's only available in sbt. On the other hand, sbt versions prior to 1.6.0-M1 did not have full support for the Rebuild Project functionality, sometimes causing IntelliJ to hang.

If you're using an sbt version prior to 1.4 - use the bloop option when importing your project. Otherwise, please upgrade to the latest sbt for better support.

### Getting Started

The following steps will work for IntelliJ IDEA 2020.1 and up, however it is highly recommended you use the latest available IntelliJ (2021.2.2 at the time of writing), as well as **at least sbt 1.6.0-M1**, if possible, otherwise some things may not work.

Here are the steps to import your sbt project into IntelliJ as a BSP project:

#### Step 0 - delete existing BSP/bloop metadata

To ensure import operation succeeds, first **delete** the following directories in your project's root:

```
$ rm -rf .bloop
$ rm -rf .bsp
```

#### Step 1 - import from existing sources

To import the project as BSP, close the current project, and IntelliJ will return to the Welcome screen. In this screen, press the **Find Action** shortcut (<kbd>⇧⌘A</kbd> on macOS, <kbd>Ctrl+Shift+A</kbd> on Windows/Linux), and type `existing`, OR go to **File | New | Project from existing sources** in the menu, when you have a project open:

{{ image(path="1-import-existing-welcome.jpg", alt="800") }}

Select **Import Project from Existing Sources**, and select the `build.sbt` of the project you wish to import. The following dialog will appear:

{{ image(path="2-project-model.jpg", alt="500") }}

Select **BSP** and press Next. Yet another dialog will appear, asking you how to import the project (i.e. which BSP engine to use, sbt native or bloop):

{{ image(path="3-sbt-or-bloop.jpg", alt="500") }}

Select **sbt (recommended)** and press Finish. IntelliJ will begin syncing the project with BSP.

#### Step 2 - enable compile on save

To really take advantage of BSP builds, enable the **Build on Save** feature in Settings. Go to **Preferences | Build, Execution, Deployment | Build Tools | BSP** and check the **build automatically on file save**. Please note, this setting is stored per-project, so when importing other projects (or re-importing the current one), it will have to be enabled again.

{{ image(path="4-build-on-save.png", alt="500") }}

Tip: it is also recommended to disable **Automatically show first error in editor**, to prevent IntelliJ jumping to the error location in case of a compilation error. To disable, go to **Preferences | Build, Execution, Deployment | Compiler** and uncheck the option. Note that this option can be stored globally, so if you want it to apply to all future projects, do this action from the Welcome screen, when no other projects are opened.

{{ image(path="5-first-error.jpg", alt="500") }}

**And that's it!** You can now continue working normally, except each time you save your current file, BSP will automatically build the changed module and will let you know immediately if there are any compilation errors. This is very similar to running with `~compile` enabled in sbt, except better integrated into the IDE, and much faster! You can see the build progress in the **Build Output** tab inside the IDE:

{{ image(path="bsp-compile.png", alt="500") }}

Here it is in action: changing the code and pressing Save will trigger immediate compilation of the changed module, showing actual compilation errors in the window:

{{ image(path="live.gif") }}

This workflow tremendously improves the feedback cycle I get from writing Scala, ensuring I know whether my code compiles or not (even when IntelliJ might sometimes claim otherwise!)

### Troubleshooting

In some rare occasions, IntelliJ might lose sync and/or stop building the project completely. When this happens, there are several things you might try:

#### Stop the BSP connection and try again

On the status bar, click the blue BSP Connection icon, and select **Stop all BSP connections**:

{{ image(path="stop-bsp-connections.png", alt="500") }}

Afterwards, try rebuilding the project or sync the bsp using the sync button in the bsp tab:

{{ image(path="sync-bsp.png", alt="500") }}

In addition, it might be useful to enable BSP tracing to log all the protocol output. To enable, go to **Preferences | Build, Execution, Deployment | Build Tools | BSP**, and enable the BSP trace log. The log will be available in the IntelliJ log directory, which can be opened from the **Help | Show Log in Finder** menu.

If this still fails, try re-importing the bsp project using the steps outlined above (including deleting the `.bloop` and `.bsp` directories).