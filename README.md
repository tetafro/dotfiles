# Dotfiles

A collection of dotfiles and scripts I use for customizing my OS.

## Install

```sh
mkdir -p $HOME/.bash-completion
mkdir -p $HOME/.local/bin

ln -sf $PWD/home/.bash_aliases ~
ln -sf $PWD/home/.bashrc ~
ln -sf $PWD/home/.inputrc ~
ln -sf $PWD/home/.profile ~
ln -sf $PWD/home/.flake8 ~
ln -sf $PWD/home/.gitconfig ~
ln -sf $PWD/home/.gitignore ~
ln -sf $PWD/home/.golangci.yml ~
ln -sf $PWD/home/.tfswitch.toml ~
ln -sf $PWD/home/.tmux.conf ~
ln -sf $PWD/home/.config/starship.toml ~/.config/
ln -sfn $PWD/home/.config/mpv ~/.config/
ln -sfn $PWD/home/.config/sublime-text/Packages/User ~/.config/sublime-text/Packages/User
ln -sf $PWD/home/.local/bin/* $HOME/.local/bin/

# Only for work
./work/install.sh
```
