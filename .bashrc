# ~/.bashrc: executed by bash for non-login shells.

# If not running interactively, don't do anything
case $- in
    *i*) ;;
    *) return;;
esac

# History settings.
HISTCONTROL=ignoreboth
HISTSIZE=1000
HISTFILESIZE=2000

# Append to the history file, don't overwrite it.
shopt -s histappend

# Check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# Make less more friendly for non-text input files.
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# Set variable identifying the chroot you work in (used in the prompt below).
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# Set a fancy prompt (non-color, unless we know we "want" color).
case "$TERM" in
    xterm|xterm-color|*-256color) color_prompt=yes;;
esac

# Force colored prompt.
force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
	color_prompt=yes
fi

if [ "$color_prompt" = yes ]; then
    time='\[\e[32m\]\t\[\e[m\]'
    chroot='${debian_chroot:+($debian_chroot)}'
    dir='\[\e[01;34m\]\w\[\e[m\]'
    prompt_symbol='\[\e[34m\]\\$\[\e[m\]'
    PS1="$time $dir $prompt_symbol "
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h \w \$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to current directory.
case "$TERM" in
    xterm*|rxvt*)
        PS1="\[\e]0;\W\a\]$PS1"
    ;;
    *)
    ;;
esac

# Enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
    if [ -f /usr/share/bash-completion/bash_completion ]; then
        . /usr/share/bash-completion/bash_completion
    elif [ -f /etc/bash_completion ]; then
        . /etc/bash_completion
    fi
fi

if [ -x /usr/bin/mint-fortune ]; then
     /usr/bin/mint-fortune
fi

# Paths settings.
if [ -d "$HOME/dev/projects/go" ] ; then
    export GOPATH="$HOME/dev/projects/go"
fi
if [ -d "/usr/local/go/bin" ] ; then
    export PATH="/usr/local/go/bin:$PATH"
fi
if [ -d "$GOPATH/bin" ] ; then
    export PATH="$GOPATH/bin:$PATH"
fi
if [ -d "$HOME/.local/bin" ] ; then
    export PATH="$HOME/.local/bin:$PATH"
fi

# Kubernetes autocomplete.
if [ -f "$HOME/.kube/kubectl.completion.bash" ]; then
    source $HOME/.kube/kubectl.completion.bash
fi
if [ -f "$HOME/.kube/k.completion.bash" ]; then
    source $HOME/.kube/k.completion.bash
fi

# Commons.
alias rm='rm -iv'
alias cp='cp -iv'
alias mv='mv -iv'
alias mkdir='mkdir -pv'
alias ls='ls -1 --color=tty'
alias grep='grep --color'
alias ping='ping -c 1'
alias rand='cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1'
# External tools.
alias k='kubectl'
alias tmx='tmux attach -t main || tmux new -s main'
alias vpn="sudo openvpn --config $HOME/.inet.ovpn"
