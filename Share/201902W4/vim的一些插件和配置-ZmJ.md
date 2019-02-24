这几天搞了一下 vim，使用Vundle管理插件，并加了一些插件及配置

### 效果图

![效果图](http://picture.wzmmmmj.com/vim-config.jpg)

> 贴下配置文件`~/.vimrc`，

```shell
set nocompatible              

" Vundle插件管理
filetype off                 
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

Plugin 'VundleVim/Vundle.vim'
Plugin 'powerline/powerline'
Plugin 'Yggdroot/indentLine'
Plugin 'tmhedberg/SimpylFold'
Plugin 'Valloric/YouCompleteMe'
Plugin 'scrooloose/syntastic'
Plugin 'scrooloose/nerdtree'
Plugin 'nvie/vim-flake8'

call vundle#end() 
" filetype on
filetype plugin indent on 
syntax enable
syntax on
colorscheme desert

" indentLine setting
let g:indentLine_enable = 1
let g:indentLine_char = '¦'
let g:indentLine_fileType = ['python']
let g:indentLine_color_term = 220
map <C-i> :IndentLinesToggle<CR>

" SimpylFold setting
let g:SimpylFold_docstring_preview=1

" NERDtree setting
let NERDTreeIgnore=['\.pyc$', '\~$']
let NERDTreeShowHidden=1
map <C-t> :NERDTreeToggle<CR> 


" syntastic
let g:syntastic_error_symbol='>>'
let g:syntastic_warning_symbol='>'
let g:syntastic_check_on_open=1
let g:syntastic_check_on_wq=0
let g:syntastic_enable_highlighting=1
let g:syntastic_python_checkers=['flake8', 'pylint', 'python3']
highlight SyntasticErrorSign ctermfg=220 ctermbg=8 guifg=white guibg=black

" to see error location list
let g:syntastic_always_populate_loc_list = 0
let g:syntastic_auto_loc_list = 0
let g:syntastic_loc_list_height = 7
map <C-s> :SyntasticToggle<CR>
function! ToggleErrors()
    let old_last_winnr = winnr('$')
    lclose
    if old_last_winnr == winnr('$')
        " Nothing was closed, open syntastic error location panel
        Errors
    endif
endfunction
nnoremap <Leader>s :call ToggleErrors()<cr>
nnoremap <Leader>sn :lnext<cr>
nnoremap <Leader>sp :lprevious<cr>

" YouCompleteMe
let g:ycm_key_list_stop_completion = ['<CR>']
highlight PMenu ctermfg=232 ctermbg=247  guifg=black guibg=darkgrey
highlight PMenuSel ctermfg=60 ctermbg=8 guifg=darkgrey guibg=black        

" index
set nu
set relativenumber

" tab
set shiftwidth=4
set tabstop=4
set softtabstop=4
set expandtab
set autoindent
set shell=/bin/bash

" other
set hlsearch
set incsearch
set smartindent
set encoding=utf-8
set backspace=2
" set cursorline

" Enable floding
set foldmethod=indent
set foldlevel=99
nnoremap <space> za
```

