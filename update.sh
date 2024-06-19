#!/bin/bash
# 
# minimal dotfile manager
# tracks files / copies them into the repo, sorted by hostname
#
# note: assumes pwd is this repo before running this script
set -u

# array of files/dirs [relative to home] to include
DOTS=(
        '.bashrc'
        # '.shell_aliases'  # needs cleaned up first
        '.vimrc'
        '.config/fuzzel'
        '.config/nvim/init.vim'
        '.config/nvim/coc-settings.json'
        '.config/autostart-i3ipc.yml'
        '.config/sway'
)

# to avoid hacky pwd/dirname stuff w/ $0 [for now?], inline the path to the repo where copies are held
DOT_DIR="${HOME}/git/dot"

# ensure the host running this script/updating dotfiles has a directory within the repo
HOST_DIR="${DOT_DIR}/${HOSTNAME}"
[ -d "$HOST_DIR" ] || mkdir -v "$HOST_DIR"

# begin dotfile processing - ensure structure is retained, naively copy w/ rsync. rely on Git to tell us about changes.
# TODO: reconsider, edge cases?
for DOT in "${DOTS[@]}"; do
        DEST="${HOST_DIR}/$DOT"
        echo "Copying '$HOME/$DOT' to '$DEST'"
        rsync -aqv "$HOME/$DOT" "$DEST" || echo "Couldn't copy '$DOT', got rc: $?"
done
