#!/bin/bash
# Replace real system files with symlinks to this repo.

mkdir -p $HOME/.bash-completion
mkdir -p $HOME/.local/bin

for item in $(ls -A ./home/); do
    if [[ -f ./home/$item ]]; then
        ln -sf "$PWD/home/$item" ~/$item
    fi
done

for item in $(ls -A ./home/.local/bin); do
    ln -sf "$PWD/home/.local/bin/$item" ~/.local/bin/$item
done

ln -sfn $PWD/home/.config/mpv ~/.config/mpv
rm -rf ~/.config/sublime-text/Packages/User
rm -rf ~/.config/sublime-text/Packages/Default
ln -sfn $PWD/home/.config/sublime-text/Packages/User ~/.config/sublime-text/Packages/User
ln -sfn $PWD/home/.config/sublime-text/Packages/Default ~/.config/sublime-text/Packages/Default

# Codex doesn't work with symlinks
mkdir -p ~/.codex
ln -f "$PWD/home/.codex/config.toml" ~/.codex/config.toml
if [[ ! -f ~/.codex/local.config.toml ]]; then
    touch ~/.codex/local.config.toml
fi

mkdir -p ~/.pi/agent
for item in $(ls -A ./home/.pi/agent); do
    ln -sf "$PWD/home/.pi/agent/$item" ~/.pi/agent/$item
done

dconf load /org/gnome/terminal/ < $PWD/home/dconf/gnome-terminal.txt

# Custom script for work files
if [[ -f ./work/install.sh ]]; then
    ./work/install.sh
fi
