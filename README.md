# Dotfiles

A collection of dotfiles and scripts I use for customizing my OS.

## Install

Linux
```sh
cp configs/* linux/configs/* $HOME
mv $HOME/vlcrc $HOME/.config/vlc/
mv $HOME/starship.toml $HOME/flake8 $HOME/.config/

mkdir -p $HOME/.local/bin
ln -s "$PWD"/tools/* "$PWD"/linux/tools/* $HOME/.local/bin/
```

MacOS
```sh
cp configs/* macos/configs/* $HOME
mv $HOME/vlcrc $HOME/Library/Preferences/org.videolan.vlc/
mv $HOME/starship.toml $HOME/flake8 $HOME/.config/

mkdir -p $HOME/.local/bin
ln -s "$PWD"/tools/* "$PWD"/macos/tools/* $HOME/.local/bin/
```
