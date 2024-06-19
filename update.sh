#!/bin/bash
# 
# minimal dotfile manager
# tracks files / copies them into the repo, sorted by hostname
#
# note: assumes pwd is this repo before running this script
set -u

# array of files [relative to home] to include
DOTS=(
        '.vimrc'
        '.config/nvim/init.vim'
        '.config/nvim/coc-settings.json'
        '.config/autostart-i3ipc.yml'
        '.config/sway'
)

# to avoid hacky pwd/dirname stuff w/ $0 [for now?], inline the path to the repo where copies are held
DOT_DIR="${HOME}/git/dot"

# ensure the host running this script/updating dotfiles has a directory
# ... then temporarily change into it for working, or exit. 
# if it couldn't be made/entered [for whatever reason], we won't be able to copy.
[ -d "$HOSTNAME" ] || mkdir -v "$HOSTNAME"

# now that the host/working dir is managed, process the dotfiles
# ensure their directory structure is retained, naively copy w/ rsync - relying on Git to tell us about changes
# TODO: reconsider, edge cases?
for DOT in "${DOTS[@]}"; do
        DEST="${DOT_DIR}/${HOSTNAME}/$DOT"
        echo "Copying '$HOME/$DOT' to '$DEST'"
        rsync -aqv "$HOME/$DOT" "$DEST" || echo "Couldn't copy '$DOT', got rc: $?"
done
