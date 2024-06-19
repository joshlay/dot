#!/usr/bin/env python3
'''simple screen locker for Sway, run by $mod+l'''
from os import environ
from i3ipc import Connection


def lock_session(manager):
    '''function for the lock sequence
    pauses any playing media and runs swaylock to lock the session'''

    lock_commands = ['playerctl pause',
                     'swaylock -f']

    for command in lock_commands:
        print(f'Executing: {command}')
        manager.command(f'exec {command}')


try:
    # explicitly tied to sway/swaysock
    #   don't get the impression swaylock works w/ i3
    #   ...which this module also supports/would use naively
    SWAYSOCK = environ['SWAYSOCK']

    # use subprocess/xrandr to get the 4k display to (later) make it primary
    # otherwise games seem to get confused on monitor/resolution


    # with the socket, connect and lock
    _wm = Connection(socket_path=SWAYSOCK, auto_reconnect=True)
    lock_session(_wm)

    # clean up, disconnect from WM
    _wm.main_quit()

except IOError as e:
    # Handle exceptions related to the connection
    print("There was a problem establishing the connection, socket:", SWAYSOCK)
    print(e)

except KeyError:
    print('The "SWAYSOCK" var is not defined')
