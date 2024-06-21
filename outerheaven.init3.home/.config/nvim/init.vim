set mouse=
set expandtab  " use spaces instead of \t
set autoindent  " match indentation of previous line
set runtimepath^=/usr/share/vim/vimfiles runtimepath+=~/.vim runtimepath+=~/.vim/after 
let &packpath = &runtimepath
source ~/.vimrc

if (has("termguicolors"))
 set termguicolors
endif
