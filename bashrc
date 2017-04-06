
alias 'ls=ls -C  -F --color=auto'
alias 'la=ls -a'
alias 'll=ls -l'

export PATH=$PATH:${HOME}/usr/bin:${HOME}/usr/sbin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${HOME}/usr/lib

export WINEDLLOVERRIDES='winemenubuilder.exe=d'

export EDITOR=vim

alias 'vi=vim'
export CSCOPE_EDITOR=vim

alias 'grep=grep --color=auto'
alias 'egrep=egrep --color=auto'
alias 'fgrep=fgrep --color=auto'

alias 'rm=rm -i'
alias 'mv=mv -i'


#export PS1="\[\033[00;31m\]\u@\h\[\033[01;32m\] \w\[\033[00;33m\][\d \t ]\[\033[00m\]$ "
#export PS1="\[\033[01;32m\][\d \t \u@\h]\[\033[00m\]$ "
export PS1="\[\033[01;31m\][\d \t \u@\h \W]\[\033[00m\]$ "

alias 'h=history'

export HISTFILE="/tmp/.bash_history"


alias 'scrot=scrot -s'


#export TERM=linux
export TERM=screen-256color

#man() {
#	/usr/bin/man $* | \
#		col -b | \
#		vim -R -c 'set ft=man nomod nolist' -
#}

export MANPAGER="sh -c \"col -b | vim -c 'set ft=man ts=8 nomod nolist nonu' \
			-c 'nnoremap i <nop>' \
			-c 'nnoremap <Space> <C-f>' \
			-c 'noremap q :quit<CR>' -\""

export MANPATH=$MANPATH:${HOME}/usr/share/man

#export PS1="\[\033[0;37m\]\342\224\214\342\224\200\$([[ \$? != 0 ]] && 
#echo \"[\[\033[0;31m\]\342\234\227\[\033[0;37m\]]\342\224\200\")[$(if [[ ${EUID} == 0 ]]; 
#then echo '\[\033[0;31m\]\h'; else echo '\[\033[0;33m\]\u\[\033[0;37m\]@\[\033[0;96m\]\h'; 
#	fi)\[\033[0;37m\]] \342\224\200[\[\033[0;32m\]\w\[\033[0;37m\]]\n\[\033[0;37m\]\342\224\224\342\224\200\342\224\200\342\225\274 \[\033[0m\]"



alias nvlc='nvlc --no-color'
