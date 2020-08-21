# Standard tools
alias rm='rm -iv'
alias cp='cp -iv'
alias mv='mv -iv'
alias mkdir='mkdir -pv'
alias ls='ls -1 --color=tty'
alias grep='grep --color'
alias ping='ping -c 1 -W 3'
alias rand='cat /dev/urandom | tr -dc "a-zA-Z0-9" | fold -w 32 | head -n 1'
alias top='top -d 30'
alias htop='htop -d 30'

# External tools
alias k='kubectl'
alias kc='kubectl config use-context'
alias kcc='kubectl config current-context'
alias tmx='tmux attach -t main || tmux new -s main'
alias vpn="sudo openvpn --cd $HOME/.config/openvpn/home --config config.ovpn"
alias venv='if [ -d ./venv ]; then source venv/bin/activate; else virtualenv -p python3 venv && source venv/bin/activate; fi'
alias go-cover='go test -coverprofile=./profile.out ./... && go tool cover -html=./profile.out'
