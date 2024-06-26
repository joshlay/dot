#!/bin/bash
# scripted note organizer/taker
#
# with Sway/on login:
#   a Kitty session is started which runs *this* script through a 'session file' in a pane
#   ultimately, providing an editor with timely notes for this week (and last) in tabs
#
# Kitty session config:
#   # ~/.config/kitty/sessions/triplesplit.conf
#   layout tall
#   launch --location=hsplit --cwd=current bash
#   launch --location=hsplit --cwd=current bash
#   launch --location=hsplit --cwd=current note-taker.sh
#
# the last command is *this script* in ~/.local/bin, presumably in $PATH already
#
SCRIPT_NAME=$(basename "$0")

# Check if the script is already running/controlling editors
if pgrep -f "$SHELL.*$SCRIPT_NAME"  | grep -v $$ > /dev/null; then
    echo "The notes are already being edited elsewhere."
    exit 1
fi

# Where are notes held? Can be overridden outside of the script; defaults to ~/notes
NOTE_DIR="${NOTE_DIR:-${HOME}/notes}"

# Get the current year and week number, used for the name of the file. eg: 2023-week40
CURRENT_NOTE=$(date +%Y-week%V)

# Get the year and week number for the same day of the previous week
LAST_WEEK_NAME=$(date -d '7 days ago' +%Y-week%V)

# Construct the two note files to open in tabs as one array
NOTE_PATHS=("$NOTE_DIR/$CURRENT_NOTE" "$NOTE_DIR/$LAST_WEEK_NAME")

# Use EDITOR variable or fallback to vim as default. If contains "vim" (like {g,n,}vim and so on), add tab arguments.
EDITOR="${EDITOR:-vim}"
if [[ $EDITOR == *vim* ]]; then
    # Run the vim-like editor with tabs
    $EDITOR -c ':tab all' "${NOTE_PATHS[@]}"
else
    # Run the editor without vim tab arg; assume array is fine
    $EDITOR "${NOTE_PATHS[@]}"
fi
