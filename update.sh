#!/bin/bash
# 
# minimal dotfile manager
# tracks files / copies them into the repo, sorted by hostname
#
# known limitations/problems:
#   - new top level directories (ie: '.config', '.local') may need to be created/seeded for new hosts
#   - failure to put slashes after directories may lead to them being nested on re-runs
#
set -u

# array of files/dirs [relative to home] to include
DOTS=(
        '.bashrc'
        '.gtkrc-2.0'
        '.gtkrc-2.0-kde4'
        # '.shell_aliases'  # needs cleaned up first
        '.vimrc'
        '.config/cava/'
        '.config/fuzzel/'
        '.config/fontconfig'
        '.config/kitty/'
        '.config/nvim/init.vim'
        '.config/nvim/coc-settings.json'
        '.config/autostart-i3ipc.yml'
        '.config/sway/'
        '.config/swayidle/config'
        '.config/swaylock/config'
        '.local/bin/backup_home'
        '.local/bin/note-taker.sh'  # run by Kitty in a 'triplesplit' session, one of many of autostart 'wants' in '...-i3ipc.yml' above
        '.vim/autoload/'  # vim-plug, mainly
        # Until I find/make custom modules worthwhile, including *only* the config/styling
        '.config/waybar/config'
        '.config/waybar/modules/settings.json'
        '.config/waybar/styles/'
        '.config/waybar/style.css'  # symlink to the wanted stylesheet (in the 'styles' dir')
        # '.gnupg/trezor/gpg.conf'  # no longer using GPG to sign commits, instead: SSH. also... now using a known phrase for 'pass'
)

# to avoid hacky pwd/dirname stuff w/ $0 [for now?], inline the path to the repo where copies are held
DOT_DIR="${HOME}/git/dot"

# ensure the host running this script/updating dotfiles has a directory within the repo
# then, begin dotfile processing - ensure structure is retained, naively copy w/ rsync
# at the end/out of band: rely on Git to tell us about changes. TODO: reconsider, edge cases? auto commit/push?
HOST_DIR="${DOT_DIR}/${HOSTNAME}"
[ -d "$HOST_DIR" ] || mkdir -v "$HOST_DIR"

for DOT in "${DOTS[@]}"; do
        echo "Copying '$HOME/$DOT' to '$HOST_DIR/${DOT}'"
        rsync -aqv "$HOME/$DOT" "$HOST_DIR/${DOT}" || echo "Couldn't copy '$DOT', got rc: $?"
done
