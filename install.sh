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

ln -sf $PWD/home/.config/starship.toml ~/.config/starship.toml
ln -sfn $PWD/home/.config/mpv ~/.config/mpv
rm -rf ~/.config/sublime-text/Packages/User
rm -rf ~/.config/sublime-text/Packages/Default
ln -sfn $PWD/home/.config/sublime-text/Packages/User ~/.config/sublime-text/Packages/User
ln -sfn $PWD/home/.config/sublime-text/Packages/Default ~/.config/sublime-text/Packages/Default

mkdir -p ~/.claude
for item in $(ls -A ./home/.claude); do
    ln -sf "$PWD/home/.claude/$item" ~/.claude/$item
done

mkdir -p ~/.codex
for item in $(ls -A ./home/.codex); do
    ln -sf "$PWD/home/.codex/$item" ~/.codex/$item
done

# Custom script for work files
if [[ -f ./work/install.sh ]]; then
    ./work/install.sh
fi
