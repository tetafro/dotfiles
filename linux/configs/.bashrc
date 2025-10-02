# ~/.bashrc: executed by bash for non-login shells.

# If not running interactively, don't do anything
case $- in
    *i*) ;;
    *) return;;
esac

# History settings
HISTCONTROL=ignoreboth # ignore spaces and duplicates
HISTSIZE=10000         # for one session
HISTFILESIZE=50000     # for ~/.bash_history

# Append to the history file, don't overwrite it
shopt -s histappend

# Check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS
shopt -s checkwinsize

# Make less more friendly for non-text input files
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# Generate PS1 after each command
PS1='\t \w \$ ' # default
__prompt_command() {
    local EXIT="$?" # needs to be first

    # Skip setting PS1 if it's not a colored terminal
    case "$TERM" in
        xterm|xterm-color|*-256color) ;;
        *) return ;;
    esac

    time='\[\e[32m\]\t\[\e[m\]'
    dir='\[\e[01;34m\]\w\[\e[m\]'
    prompt_symbol_color='34m'
    if [ $EXIT != 0 ]; then
        prompt_symbol_color='91m'
    fi
    prompt_symbol='\[\e['$prompt_symbol_color'\]\\$\[\e[m\]'

    prefix=''
    [ ! -z $VIRTUAL_ENV ] && prefix='(venv) '

    PS1="$prefix$time $dir $prompt_symbol "

    # Set directory name as a title for local shell tab,
    # hostname without domain - for SSH sessions
    if [[ -z $SSH_TTY ]]; then
        title=$(basename "$PWD")
    else
        title="[${HOSTNAME%%.*}]"
    fi
    echo -en "\e]0;${title}\a"
}
PROMPT_COMMAND=__prompt_command

# Enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc)
if ! shopt -oq posix; then
    if [ -f /usr/share/bash-completion/bash_completion ]; then
        . /usr/share/bash-completion/bash_completion
    elif [ -f /etc/bash_completion ]; then
        . /etc/bash_completion
    fi
fi

# Aliases
if [ -f "$HOME/.bash_aliases" ]; then
    . "$HOME/.bash_aliases"
fi

# Rust
if [ -f "$HOME/.cargo/env" ] ; then
    source "$HOME/.cargo/env"
fi

# Bash completion
if [ -d "$HOME/.bash-completion" ] ; then
    for src in "$HOME/.bash-completion/"*.sh; do
        source "$src"
    done
fi

# Work
if [ -f "$HOME/.bashrc_work" ]; then
    source "$HOME/.bashrc_work"
fi

# Run starship prompt
eval "$(starship init bash)"
