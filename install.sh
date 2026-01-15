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
ln -sfn $PWD/home/.config/sublime-text/Packages/User ~/.config/sublime-text/Packages/User

# Custom script for work files
if [[ -f ./work/install.sh ]]; then
    ./work/install.sh
fi
