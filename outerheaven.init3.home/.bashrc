# shellcheck shell=bash source=/dev/null
# Source global definitions
[ -f /etc/bashrc ] && . /etc/bashrc

# Update window size after every command
shopt -s checkwinsize

# User specific aliases, functions, and variables
[ -r ~/.shell_aliases ] && . ~/.shell_aliases
[ -r ~/.poetry_bash_completion ] && . ~/.poetry_bash_completion
export PS1="\[\e[0;34m\]\w \[\e[0;37m\]$ \[\e[0m\]"
#export PS1="\[\e[0;37m\]\u\[\e[0;37m\]:\[\e[0;34m\]\w \[\e[0;37m\]$ \[\e[0m\]"
export HISTTIMEFORMAT='%F %T %Z '
export HISTCONTROL=ignoredups:erasedups:ignorespace
# Undocumented feature which sets the size to "unlimited".
# http://stackoverflow.com/questions/9457233/unlimited-bash-history
export HISTFILESIZE=
export HISTSIZE=

[[ ${KITTY_WINDOW_ID} ]] && \
	echo ; fortune -n 180 -s | lolcat --random --24bit ; echo
