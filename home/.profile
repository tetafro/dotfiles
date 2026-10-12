# ~/.profile: executed by the command interpreter for login shells.

# Env
if [ -f /usr/bin/subl ]; then
    export EDITOR="/usr/bin/subl --wait"
elif [ -f /usr/bin/vim ]; then
    export EDITOR=/usr/bin/vim
else
    export EDITOR=/usr/bin/vi
fi

# Secrets
if [ -d "$HOME/.profile_secrets" ] ; then
    . "$HOME/.profile_secrets"
fi

# Paths settings
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
    . "$HOME/.cargo/env"
fi
if [ -d "/opt/kafka/bin" ] ; then
    export PATH="/opt/kafka/bin:$PATH"
fi
if [ -d "$HOME/.krew" ] ; then
    export PATH="$HOME/.krew/bin:$PATH"
fi

# Work
if [ -f "$HOME/.profile_work" ]; then
    source "$HOME/.profile_work"
fi

# If running bash
if [ -n "$BASH_VERSION" ]; then
    if [ -f "$HOME/.bashrc" ]; then
        . "$HOME/.bashrc"
    fi
fi
