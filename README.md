# Dotfiles

A collection of dotfiles and scripts I use for customizing my OS.

## Install

```sh
platform=$(case $(uname -s) in Darwin) echo macos;; Linux) echo linux;; esac)

cp configs/* $platform/configs/* $HOME
mv $HOME/vlcrc $HOME/.config/vlc/
mv $HOME/starship.toml $HOME/flake8 $HOME/.config/
ln -s "$PWD"/tools/* "$PWD"/$platform/tools/* $HOME/.local/bin/
```
