#!/usr/bin/env python3
"""
This script provides screenshot handling for Sway

Determines the mode (region or window), and then takes a capture

Expects window manager keybinds like below:
  bindsym --no-repeat Print exec "~/.config/sway/scripts/screenshot.py region"
  bindsym --no-repeat Shift+Print exec "~/.config/sway/scripts/screenshot.py window"

If mode is 'region', the tool 'slurp' is used to select the region to capture.

If mode is 'window', the WM is asked which display is active (to capture).

In both cases, the 'grim' utility does the image capture. Captures go here:
  ~/Pictures/screenshots/Screenshot_*.png

Fedora dependencies:
 - sudo dnf in python-{i3ipc,pillow}

Note: while i3ipc aspects of this will work with i3...
      slurp/grim likely will not
"""
import argparse
import os
import subprocess
from time import strftime
from i3ipc import Connection, Event
from PIL import Image
from PIL.PngImagePlugin import PngInfo

# setup argparse
# take one arg, m/mode: selection/window
parser = argparse.ArgumentParser(
        description='Take some screenshots for Sway using IPC and slurp/grim')

# add main arg, screenshot mode -- region (selection area) or [focused] window
parser.add_argument('mode', type=str, choices=['region', 'window', 'w', 'r'],
                    help='''Screenshot "mode", either:
                    A selected area ('region') or
                    the focused display ('window')"''')

# instantiate args
args = parser.parse_args()

# env prep
# get the current time
now = strftime("%Y-%m-%dT-%H%M%z")
# use strftime - similar iso format as 'datetime', with 1 minor fix
# no ':' - in the off chance they are uploaded to Jira
# ex: 2022-11-21T-2337-0600

# set a var for the homedir using os.environ -  arguably not portable? /shrug
homedir = os.environ['HOME']
screenshot_dir = f'{homedir}/Pictures/screenshots'
screenshot_path = f'{screenshot_dir}/Screenshot_{now}.png'
preview_command = f"imv -d -s none '{screenshot_path}'"
# preview_command = f"xdg-open '{screenshot_path}'"

if not os.path.isdir(screenshot_dir):
    print(f"Screenshot dir doesn't exist, creating {screenshot_dir}")
    os.mkdir(screenshot_dir)
else:
    print(f'Screenshot dir ({screenshot_dir}) exists, continuing')

# misc functions
def determine_ss_cmd():
    '''based on mode, determine the screenshot command'''
    # screenshot command handling (based on mode)
    # grim uses compression level 1 in both cases
    # neglible quality difference while saving space
    if args.mode in ['window', 'w']:
        # use wm connection to determine the active output
        outputs = _wm.get_outputs()
        for output in outputs:
            if output.focused:
                active_output = output.name
        print(f'determined active output: {active_output}')
        command = f"grim -l 1 -c -o {active_output} '{screenshot_path}'"
    elif args.mode in ['region', 'r']:
        # omits -c to leave out cursors
        command = f"slurp -d | grim -l 1 -g - '{screenshot_path}'"
    return command

def preview_focus(_wm, _event):
    '''function called by window manager new_window events
    checks if new window is preview, if so: give it focus'''
    if _event.container.app_id == 'imv':
        # give the preview focus
        # for Sway we use 'app_id', for i3 this is probably 'class'
        _wm.command('[app_id=imv] focus')
        # once the preview window is focused, close our connection to the wm
        _wm.main_quit()

def wm_connect():
    '''get the party started, create a connection to the window manager'''
    conn = Connection(auto_reconnect=True)
    # on new window events check if screenshot preview window gets focus
    conn.on(Event.WINDOW_NEW, preview_focus)
    return conn

def _run_command(command):
    print(f'Command: {command}')
    _r = subprocess.run(command, shell=True, capture_output=True, check=False)
    if _r.stderr:
        raise subprocess.CalledProcessError(
                returncode = _r.returncode,
                cmd = _r.args,
                stderr = _r.stderr
                )
    if _r.stdout:
        print(f"Command Result: {_r.stdout.decode('utf-8')}")
    return _r

# begin screenshot/preview process
# connect to the window manager -- Sway
# (i3 could work, may need grim/slurp replacements)
_wm = wm_connect()
# determine screenshot command - differs if window or region mode
screenshot_command = determine_ss_cmd()

# run the screenshot/preview commands
# previewing/sending focus only if screenshot is taken
SS_RC = -1
try:
    ss_result = _run_command(screenshot_command)
    SS_RC = ss_result.returncode
except subprocess.CalledProcessError as error:
    print('screenshot failed/aborted')
    # clean up after ourselves, close the wm loop
    _wm.main_quit()

# if the screenshot succeeded, place a comment on the image
# and then preview/focus the window
if SS_RC == 0:
    #
    # construct the comment for the screenshot
    # immediately after it's taken, find the focused window details
    wm_tree = _wm.get_tree()
    wm_focused = wm_tree.find_focused()
    app_name = wm_focused.name
    app_id = wm_focused.app_id
    COMMENT = f"Screenshot of '{app_name} (app_id: {app_id}) at {now}'"
    print(f'storing comment: {COMMENT}')
    #
    # open the screenshot for (metadata) modification
    # adding the application title/window class/date as a comment
    # visible using 'exiftool', easier sorting through command line
    ss_obj = Image.open(screenshot_path)
    ss_metadata = PngInfo()
    ss_metadata.add_text("Comment", COMMENT)
    #
    # write the (commented) image back out
    ss_obj.save(screenshot_path, pnginfo=ss_metadata)
    #
    # open the preview with 'imv'
    print(f"exec preview: {preview_command}")
    _wm.command(f'exec {preview_command}')
    #
    # start the main loop for the window manager
    # basically wait for the preview listener to fire
    # when the preview window opens, a message is sent to give it focus
    # afterwards we exit
    _wm.main()
