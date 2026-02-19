+++
title = "Setting up a Haskell development environment in minutes in Visual Studio Code"
date = 2020-02-01T13:58:22Z
+++
This was initially a long post, detailing all the manual steps required to set up a complete Haskell development environment, however, thanks to a [hint](https://twitter.com/k_cieslak/status/1222115319881310210) by [Krzysztof Cieślak](https://twitter.com/k_cieslak), this process is now fully automated, allowing you to get started in *minutes*. All thanks to a Visual Studio Code feature called *devcontainers*, supporting running the [development environment in a Docker container](https://code.visualstudio.com/docs/remote/containers).

<!-- more -->

#### Prerequisites
1. Visual Studio Code with [Remote Development extension pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)
2. Docker Desktop v2.0+ (requires Windows 10 Pro/Enterprise)
3. Initial Docker setup, detailed here: https://code.visualstudio.com/docs/remote/containers
3. The [`haskell-hie-devcontainer`](https://github.com/hmemcpy/haskell-hie-devcontainer), by yours truly!

#### Docker configuration

Install [Docker Desktop](https://www.docker.com/products/docker-desktop), and configure it according to the steps detailed in [the documentation](https://code.visualstudio.com/docs/remote/containers) for remote development. This requires sharing the directory containing your source code with Docker, and this feature is only available via the Docker Desktop UI. Once you're done, install the [Remote Development extension pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) in Visual Studio Code.

#### Preparing your project

To set up your project, download the contents of [this repository](https://github.com/hmemcpy/haskell-hie-devcontainer), and place the `.devcontainer` directory in the root of your project, and restart Visual Studio Code.

Provided you've set it up correctly, the next time Visual Studio Code starts, it will prompt you to reload your project in the container:

{{ image(path="devcontainer.png") }}

Pressing the **Reopen in Container** button will reload your project, and perform the automated steps to download and configure the Docker image for Haskell development.

{{ image(path="haskell-ide.png") }}

Note that the initial download might take a few moments.

#### Technical details

The `.devcontainer` directory contains two files: the `Dockerfile` describing the image, and a `devcontainer.json` file which has some additional settings for Visual Studio Code.

The `Dockerfile` is an image based on [`hmemcpy/hie`](https://hub.docker.com/r/hmemcpy/hie) (which in turn is based on `nixos/hie`), an Alpine image which contains the following:

* The [Nix package manager](https://nixos.org/nix/)
* Configuration for [Cachix](https://cachix.org/) - a binary cache for Nix
* Glasgow Haskell Compiler (GHC) version 8.6.5
* HIE ([haskell-ide-engine](https://github.com/haskell/haskell-ide-engine)) for GHC 8.6.5

The `devcontainer.json` has some additional configuration, in particular, the required extensions that have to be installed, and the name of the remote user (must match the one in the `Dockerfile`).

Please feel free to contribute improvements to this devcontainer!

**Note**: it is quite possible that the process will be entirely automated if the `.devcontainer` configuration will be accepted to the Microsoft repository, allowing it to be configured straight from Visual Studio Code, without any additional downloads. This is currently tracked in an issue [microsoft/vscode-dev-containers#202](https://github.com/microsoft/vscode-dev-containers/issues/202). Stay tuned for updates!

#### Addendum: manual installation without Docker

If you don't want to install Docker or use devcontainers, the following steps will allow you to manually install the [haskell-ide-engine](https://github.com/haskell/haskell-ide-engine) (HIE) components, which power the IDE features in Visual Studio Code:

1. Install the [Nix package manager](https://nixos.org/nix/)
    * on Windows 10, Nix can be installed in WSL2 (requires Insiders Build 18917 or higher), or WSL after applying [these changes](https://nathan.gs/2019/04/12/nix-on-windows/)
2. Download the [Haskell Platform](https://www.haskell.org/platform/) (GHC), or install with Nix:
    *  `nix-env -i ghc-8.6.5`
3. Install [Cachix](https://cachix.org/) (binary cache for Nix)
    * `nix-env -iA cachix -f https://cachix.org/api/v1/install`
4. Configure to use `all-hies` (cached repository of all HIE builds)
    * `cachix use all-hies`
5. Install the matching HIE version for your GHC (e.g. 8.6.5):
    * `nix-env -iA selection --arg selector 'p: { inherit (p) ghc865; }' -f https://github.com/infinisil/all-hies/tarball/master`
6. Install the [Haskell Language Server](https://marketplace.visualstudio.com/items?itemName=alanz.vscode-hie-server) extension in Visual Studio Code