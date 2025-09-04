# Dotfiles

A collection of dotfiles and scripts I use for customizing my OS.

## Install

Linux
```sh
ln -sf $PWD/linux/configs/.bash_aliases ~
ln -sf $PWD/linux/configs/.bashrc ~
ln -sf $PWD/linux/configs/.inputrc ~
ln -sf $PWD/linux/configs/.profile ~
ln -sf $PWD/configs/.flake8 ~
ln -sf $PWD/configs/.gitconfig ~
ln -sf $PWD/configs/.gitignore ~
ln -sf $PWD/configs/.golangci.yml ~
ln -sf $PWD/configs/.tfswitch.toml ~
ln -sf $PWD/configs/.tmux.conf ~
ln -sf $PWD/configs/starship.toml ~/.config/
ln -sf $PWD/configs/mpv ~/.config/
ln -sf $PWD/configs/sublime-text ~/.config/sublime-text/Packages/User

# Only for work
./work/install.sh

mkdir -p $HOME/.local/bin
ln -sf $PWD/tools/* $PWD/linux/tools/* $HOME/.local/bin/
```

MacOS
```sh
cp configs/* macos/configs/* $HOME
ln -sf $PWD/configs/mpv $HOME/.config/
mv $HOME/starship.toml $HOME/flake8 $HOME/.config/

mkdir -p $HOME/.local/bin
ln -sf $PWD/tools/* $PWD/macos/tools/* $HOME/.local/bin/
```
