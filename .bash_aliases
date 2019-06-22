# Standard tools
alias rm='rm -iv'
alias cp='cp -iv'
alias mv='mv -iv'
alias mkdir='mkdir -pv'
alias ls='ls -1 --color=tty'
# alias ls='ls -1G' # macos
alias grep='grep --color'
alias ping='ping -c 1'
alias rand='cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1'
alias ts='date +%s'

# External tools
alias k='kubectl'
alias kc='kubectl config use-context'
alias kcc='kubectl config current-context'
alias tmx='tmux attach -t main || tmux new -s main'
alias vpn="sudo openvpn --config $HOME/.inet.ovpn"
