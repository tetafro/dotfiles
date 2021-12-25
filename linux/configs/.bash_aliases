# Standard tools
alias rm='rm -iv'
alias cp='cp -iv'
alias mv='mv -iv'
alias mkdir='mkdir -pv'
alias ls='ls -1 --color=tty --group-directories-first'
alias grep='grep --color'
alias ping='ping -c 1 -W 3'
alias rand='cat /dev/urandom | tr -dc "a-zA-Z0-9" | fold -w 32 | head -n 1'
alias top='top -d 30'
alias htop='htop -d 30'
alias python='python3'

# Replacements
alias ls='exa -1 --group-directories-first'
alias cat='bat -pP'

# External tools
alias k='kubectl'
alias tmx='tmux attach -t main || tmux new -s main'
alias vpn="sudo openvpn --cd $HOME/.config/openvpn/home --config config.ovpn"
alias venv='if [ -d ./venv ]; then source venv/bin/activate; else virtualenv -p python3 venv && source venv/bin/activate; fi'
alias go-test="gotest ./..."
alias go-cover='go test -coverprofile=./profile.out -coverpkg=./... ./... && go tool cover -html=./profile.out'
alias go-lint="golangci-lint run -c ~/.golangci.yml"
alias go-deps="go list -m -u -f '{{.Indirect}} {{.}}' all | grep '^false' | cut -d ' ' -f 2,3,4 | grep --color=never '\['"
