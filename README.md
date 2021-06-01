# Dotfiles

A collection of dotfiles and scripts I use for customizing my OS.

## Install

```sh
cp bash/* \
    .gitconfig \
    .gitignore \
    .golnagci.yml \
    .inputrc \
    .tmux.conf \
    $HOME
ln -s "$PWD"/tools/* $HOME/.local/bin/
cp vlc/* $HOME/.config/vlc/
cp vscode/* $HOME/.config/Code/User/
cp flake8 $HOME/.config/
cp starship.toml $HOME/.config/
```
