

syntax on
filetype indent plugin on

set fileencodings=utf-8,ucs-bom,gb18030,gbk,gb2312,cp936
set nu
set hlsearch
"set backspace=2
set ruler
set showmode
syntax on
set history=50
set nolinebreak
"set backspace=indent,eol,start
set t_Co=256

set nobackup

"set encoding=utf-8
"set guifont=*
"set guifontwide=*
set smartindent
set autoindent
set cindent


if has('gui_running')
"	winsize 100 40
	set guioptions-=m
	set guioptions-=t
	set guioptions-=M
	set guioptions-=T
	set guioptions-=r
	set guioptions-=l

"	set guifont=Droid\ Sans\ Mono\ 10
"	set guifontwide=AR\ PL\ SungtiL\ GB\ 10

	colorscheme grb256
endif

"set foldmethod=indent
"
set fileformat=unix
set fileencoding=utf-8

set expandtab
set shiftwidth=4
set tabstop=4
set softtabstop=4

"colorscheme elflord
