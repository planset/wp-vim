"let s:save_cpo = &cpo
"set cpo&vim

let s:current_file=expand('<sfile>')

python << PYTHONEOF
import os

plugin_dir = os.path.dirname(os.path.dirname(vim.eval('s:current_file')))

vim.command('let g:wp_vim_plugin_dir = "' + plugin_dir + '"')
    
PYTHONEOF

"if !exists('g:wp_vim_plugin_dir')
"  let g:wp_vim_plugin_dir = '~/.vim/bundle/wp-vim'
"endif



"
"" unite-script key mapping
"
exe 'nmap <silent> ,wec :e ' . eval('g:wp_vim_plugin_dir') . '/script/config.py<CR>'
exe 'nmap <silent> ,wl :<C-u>Unite script:python:' . eval('g:wp_vim_plugin_dir') . '/script/list_edit_draft.py<CR>'
exe 'nmap <silent> ,wpl :<C-u>Unite script:python:' . eval('g:wp_vim_plugin_dir') . '/script/list_edit_publish.py<CR>'
exe 'nmap <silent> ,wd :<C-u>Unite script:python:' . eval('g:wp_vim_plugin_dir') . '/script/list_delete.py<CR>'
exe 'nmap <silent> ,wn :<C-u>Unite script:python:' . eval('g:wp_vim_plugin_dir') . '/script/wpcontrol.py<space>new<space>-p<space>draft<space>'
exe 'nmap <silent> ,wpn :<C-u>Unite script:python:' . eval('g:wp_vim_plugin_dir') . '/script/wpcontrol.py<space>new<space>-p<space>publish<space>'

"nnoremap <silent> ,wc :<C-u>Unite script:python:~/Dropbox/private/p/wp-vim/list_categories.py<CR>

"let &cpo = s:save_cpo
"unlet s:save_cpo

