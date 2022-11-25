# Standard tools
alias rm='rm -iv'
alias cp='cp -iv'
alias mv='mv -iv'
alias mkdir='mkdir -pv'
alias ls='ls -1 --literal --color=tty --group-directories-first --human-readable --all'
alias grep='grep --color --exclude-dir=.git --binary-files=without-match'
alias root='sudo -E -s'
alias ping='ping -c 1 -W 3'
alias ping-router='ping -c 1 -W 3 192.168.178.1'
alias ping-exmaple='ping -c 1 -W 3 example.com'
alias rand='cat /dev/urandom | tr -dc "a-zA-Z0-9" | fold -w 32 | head -n 1'
alias top='top -d 30'
alias htop='htop -d 30'
alias python='python3'
alias ports='sudo ss -ntlp4 | columnt -t'

# External tools
alias k='kubectl'
alias tmx='tmux attach -t main || tmux new -s main'
alias vpn-eu="sudo openvpn --cd $HOME/.config/openvpn/home-eu --config config.ovpn"
alias vpn-ru="sudo openvpn --cd $HOME/.config/openvpn/home-ru --config config.ovpn"
alias venv='if [ -d ./venv ]; then source venv/bin/activate; else virtualenv -p python3 venv && source venv/bin/activate; fi'
alias go-deps="go list -m -u -f '{{.Indirect}} {{.}}' all | grep '^false' | cut -d ' ' -f 2,3,4 | grep --color=never '\['"
alias go-test="set -o pipefail && go test -json -count=1 -cover | tparse"
# alias go-test="gotest ./..."
alias go-cover='go test -coverpkg=./... -coverprofile=./profile.out ./... && go tool cover -html=./profile.out'
alias go-lint="golangci-lint run -c ~/.golangci.yml"
alias go-echo="go run $HOME/dev/playground/echo/main.go"
alias cat='bat --plain --paging=never'

# Directories
alias cd-playground="cd $HOME/dev/playground"
alias cd-pet="cd $HOME/dev/pet"
alias cd-opensource="cd $HOME/dev/opensource"
