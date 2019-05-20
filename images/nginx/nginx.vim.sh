#!/bin/bash
[[ -d ~/.vim/syntax ]] || mkdir  -p ~/.vim/syntax
wget http://www.vim.org/scripts/download_script.php?src_id=19394 -O ~/.vim/syntaxnginx.vim
echo "au BufRead,BufNewFile /usr/local/nginx/* set ft=nginx" >> ~/.vim/filetype.vim
