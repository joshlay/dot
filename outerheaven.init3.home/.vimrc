" NOTE: don't add more LSPs here, use 'coc.nvim' - it offers better completion
" 'vim'/common elements are held here while 'nvim' has another config: '.config/nvim/init.vim'
call plug#begin('~/.vim/exts')
" Plug 'AlexvZyl/nordic.nvim', { 'branch': 'main' }  " replaced w/ ayu
Plug 'ayu-theme/ayu-vim'
Plug 'powerman/vim-plugin-AnsiEsc'
Plug 'fladson/vim-kitty'
" replaced 'ansible-vim' that *was* here w/ dist pkg, used by 'coc-ansible'
Plug 'neoclide/coc.nvim', {'branch': 'release'}
Plug 'yaegassy/coc-ansible', {'do': 'yarn install --frozen-lockfile'}
call plug#end()

" misc. preferences
set cursorline
set nu
autocmd FileType yaml setlocal et ts=2 ai sw=2 nu sts=0
set updatetime=750
filetype plugin on
syntax on
" let ayucolor="light"
" let ayucolor="mirage"
let ayucolor="dark"
colorscheme ayu
match Error /\%xA0/

" coc.nvim/lsp setup
inoremap <silent><expr> <TAB>
      \ coc#pum#visible() ? coc#pum#next(1) :
      \ CheckBackspace() ? "\<Tab>" :
      \ coc#refresh()
inoremap <expr><S-TAB> coc#pum#visible() ? coc#pum#prev(1) : "\<C-h>"

" Make <CR> to accept selected completion item or notify coc.nvim to format
" <C-g>u breaks current undo, please make your own choice
inoremap <silent><expr> <CR> coc#pum#visible() ? coc#pum#confirm()
                              \: "\<C-g>u\<CR>\<c-r>=coc#on_enter()\<CR>"

function! CheckBackspace() abort
  let col = col('.') - 1
  return !col || getline('.')[col - 1]  =~# '\s'
endfunction

function! ShowDocumentation()
  if CocAction('hasProvider', 'hover')
    call CocActionAsync('doHover')
  else
    call feedkeys('K', 'in')
  endif
endfunction

let g:coc_filetype_map = {
  \ 'yaml.ansible': 'ansible',
  \ }

" Use K to show documentation in preview window
nnoremap <silent> K :CocCommand ansible.ansbileDoc.showInfo<CR>
