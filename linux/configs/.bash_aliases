# Standard tools
alias rm='rm -iv'
alias cp='cp -iv'
alias mv='mv -iv'
alias mkdir='mkdir -pv'
alias ls='ls -1 --literal --color=tty --group-directories-first --human-readable --all'
alias grep='grep --color --exclude-dir=.git --binary-files=without-match'
alias root='sudo -E -s'
alias ping='ping -c 1 -W 3'
alias rand='cat /dev/urandom | tr -dc "a-zA-Z0-9" | fold -w 32 | head -n 1'
alias top='top -d 30'
alias htop='htop -d 30'
alias python='python3'
alias ports='sudo ss -ntlp4 | column -t'
alias lifetime='sudo tune2fs -l $(findmnt -n -o SOURCE /) | grep "Filesystem created:"'
alias lsof-stats='for pid in /proc/[0-9]*; do \
    p=$(basename $pid); \
    printf "%4d %6d / %s\n" $(sudo ls $pid/fd | wc -l) $p "$(ps -p $p -o comm=)"; \
    done | sort -nr'

# External tools
alias code='subl'
alias sn='sync-notes'
alias cat='bat --plain --paging=never'
alias tmx='tmux attach -t main || tmux new -s main'
alias git-cleanup='git branch --merged master | \
    grep -v "master\|main" | \
    xargs --no-run-if-empty git branch -d'
alias go-deps="go list -m -u -f '{{.Indirect}} {{.}}' all | \
    grep '^false' | \
    cut -d ' ' -f 2,3,4 | \
    grep --color=never '\['"
alias go-test="set -o pipefail && go test -json -count=1 -cover | tparse"
alias go-cover='go test -coverpkg=./... \
    -coverprofile=./profile.out ./... && \
    go tool cover -html=./profile.out'
alias go-lint="golangci-lint run -c ~/.golangci.yml"
alias go-echo="go run $HOME/dev/playground/echo/main.go"
alias venv='if [ -d ./venv ]; then \
    source venv/bin/activate; \
    else virtualenv -p python3 venv && source venv/bin/activate; \
    fi'
alias k='kubectl'
alias kctx='kubectx'
alias kns='kubens'

# Directories
alias cd-dump="cd $HOME/dump"
alias cd-playground="cd $HOME/dev/playground"
alias cd-pet="cd $HOME/dev/pet"
alias cd-github="cd $HOME/dev/github"
alias cd-dotfiles="cd $HOME/dev/pet/dotfiles"
