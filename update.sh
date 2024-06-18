#!/bin/bash
# 
# minimal dotfile manager
# tracks files / copies them into the repo, sorted by hostname
#
set -u

# array of files [relative to home] to include
DOTS=(
        '.vimrc'
        '.config/nvim/init.vim'
        '.config/nvim/coc-settings.json'
        '.config/autostart-i3ipc.yml'
        '.config/sway'
)

# ensure the host running this script/updating dotfiles has a directory
# ... then temporarily change into it for working, or exit. 
# if it couldn't be made/entered [for whatever reason], we won't be able to copy.
[ -d "$HOSTNAME" ] || mkdir -v "$HOSTNAME"
pushd "$HOSTNAME" || exit

echo "Changed working dir to $PWD"

# now that the host/working dir is managed, process the dotfiles
# ensure their directory structure is retained, then recursively copy
for DOT in "${DOTS[@]}"; do
        DOT_DIR="$(dirname "$DOT")"
        [ -d "$DOT_DIR" ] || mkdir -vp "$DOT_DIR"
        # naively 'copy' with rsync; rely on git to tell us about changes. TODO: reconsider
        echo "Copying '$HOME/$DOT' to '$DOT'"
        rsync -aqv "$HOME/$DOT" "$DOT" || echo "Couldn't copy '$DOT', got rc: $?"
done

# return where we were
popd || exit
