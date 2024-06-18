set mouse=
" use spaces instead of \t
set expandtab
" match indentation of previous line
set autoindent
set runtimepath^=~/.vim runtimepath+=~/.vim/after
let &packpath = &runtimepath
source ~/.vimrc

if (has("termguicolors"))
 set termguicolors
endif
