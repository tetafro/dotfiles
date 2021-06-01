# Aliases.
if [ -f "$HOME/.zsh_aliases" ]; then
    . "$HOME/.zsh_aliases"
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

# Run starship prompt.
eval "$(starship init zsh)"
