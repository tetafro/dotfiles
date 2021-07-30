# Aliases.
if [ -f "$HOME/.zsh_aliases" ]; then
    . "$HOME/.zsh_aliases"
fi

# Read inputrc.
if [ -f "$HOME/.inputrc" ]; then
    . "$HOME/.inputrc"
fi

# Paths settings.
if [ -d "$HOME/.local/bin" ]; then
    export PATH="$HOME/.local/bin:$PATH"
fi
if [ -d "/usr/local/go/bin" ]; then
    export PATH="/usr/local/go/bin:$PATH"
fi
if [ -d "$HOME/.go" ]; then
    export GOPATH="$HOME/.go"
fi
if [[ ! -z $GOPATH && -d "$GOPATH/bin" ]]; then
    export PATH="$GOPATH/bin:$PATH"
fi
if [ -d "$HOME/.cargo/bin" ]; then
    export PATH="$HOME/.cargo/bin:$PATH"
fi
if [ -d "/opt/kafka/bin" ]; then
    export PATH="/opt/kafka/bin:$PATH"
fi
if [ -d "/usr/local/opt/mysql-client/bin" ]; then
    export PATH="/usr/local/opt/mysql-client/bin:$PATH"
fi

# Change word delimiters.
autoload -U select-word-style
select-word-style bash

# Enable autocompletion.
autoload -Uz compinit && compinit

# Fix autocompletion for makefiles.
zstyle ':completion:*:*:make:*' tag-order 'targets'

# kubectl autocomplete.
if [ -f "$HOME/.kube/kubectl.completion.zsh" ]; then
    source $HOME/.kube/kubectl.completion.zsh
fi
if [ -f "$HOME/.kube/k.completion.zsh" ]; then
    source $HOME/.kube/k.completion.zsh
fi

# kaf autocomplete.
if [ -f "$HOME/.kaf/completion.zsh" ]; then
    source $HOME/.kaf/completion.zsh
fi

# Go.
# export GOFLAGS='-mod=vendor'

# Rust.
if [[ -f "$HOME/.cargo/env" ]]; then
    . "$HOME/.cargo/env"
fi

# Run starship prompt.
eval "$(starship init zsh)"
