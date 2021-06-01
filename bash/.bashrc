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

# Generate PS1 after each command.
PS1='\t \w \$ ' # default
__prompt_command() {
    local EXIT="$?" # needs to be first

    # Skip setting PS1 if it's not a colored terminal.
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

    # Set directory name as a title for shell tab.
    title=$(basename "$PWD")
    echo -en "\e]0;${title}\a"
}
PROMPT_COMMAND=__prompt_command

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

# Aliases.
if [ -f "$HOME/.bash_aliases" ]; then
    . "$HOME/.bash_aliases"
fi

# Paths settings.
if [ -d "$HOME/.local/bin" ] ; then
    export PATH="$HOME/.local/bin:$PATH"
fi
if [ -d "/usr/local/go/bin" ] ; then
    export PATH="/usr/local/go/bin:$PATH"
fi
if [ -d "$HOME/.go" ] ; then
    export GOPATH="$HOME/.go"
fi
if [ -d "$GOPATH/bin" ] ; then
    export PATH="$GOPATH/bin:$PATH"
fi
if [ -d "$HOME/.cargo/bin" ] ; then
    export PATH="$HOME/.cargo/bin:$PATH"
fi
if [ -d "/opt/kafka/bin" ] ; then
    export PATH="/opt/kafka/bin:$PATH"
fi

# kubectl autocomplete.
if [ -f "$HOME/.kube/kubectl.completion.bash" ]; then
    source $HOME/.kube/kubectl.completion.bash
fi
if [ -f "$HOME/.kube/k.completion.bash" ]; then
    source $HOME/.kube/k.completion.bash
fi

# kaf autocomplete.
if [ -f "$HOME/.kaf/completion.bash" ]; then
    source $HOME/.kaf/completion.bash
fi

# Go.
# export GOFLAGS='-mod=vendor'

# Run starship prompt.
eval "$(starship init bash)"
