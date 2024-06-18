#!/usr/bin/env python3
'''Manages PulseAudio volume for a sink (output) by percentage

Run by Sway on XF86Audio{Raise,Lower}Volume'''
import argparse
import pulsectl
from pydbus import SessionBus

def get_pulse():
    '''Returns a Pulse object for inspection/modification'''
    return pulsectl.Pulse('volume-changer')

def get_sink(pulse, sink_name=None):
    '''Get / return a PulseAudio sink (output) object by name.

    Used to query and set the volume. If `sink_name` is omitted, return *default*

    Args:
        pulse (Pulse): The Pulse object to query, see `get_pulse()`
        sink_name (str, optional): The name of the PulseAudio sink to look for.
                If omitted the default sink is assumed

    Returns:
        pulsectl.PulseSinkInfo'''
    if sink_name is None:
        return pulse.get_sink_by_name(pulse.server_info().default_sink_name)
    return pulse.get_sink_by_name(sink_name)

def get_volume_rounded(pulse, sink):
    '''Return the volume of the provided sink

    Returned as a rounded int averaged across channels, assumed linked'''
    return round(pulse.volume_get_all_chans(sink) * 100)

def set_volume(pulse, sink, adjustment):
    '''Changes the PulseAudio `sink` volume by the given `adjustment`

    `sink` should be a pactl object; see `get_sink`

    `adjustment` should be a float, ie 0.01 for *raising* 1%
        Invert (* -1) to lower'''
    pulse.volume_change_all_chans(sink, adjustment)

# Create argument parser
parser = argparse.ArgumentParser(description='Change audio volume.')
parser.add_argument('direction', choices=['raise', 'lower'], help='The direction to change the volume.')
parser.add_argument('percentage', nargs='?', default=1, type=int, help='The percentage to change the volume.')
parser.add_argument('--sink', default=None, help='The PulseAudio sink (name) to manage.')

# Parse arguments
args = parser.parse_args()
# Calculate the volume change as a float, inverse it if *lowering*
# used as a multiplier
change = args.percentage / 100
if args.direction == 'lower':
    change = change * -1

# construct empty dict for JSON output/data
# interesting info is appended later
data = {"sink": "",
          "change": "",
          "start_vol": "",
          "new_vol": ""}

# connect to the notification bus
notifications = SessionBus().get('.Notifications')

# get pulse / connect
try:
    with get_pulse() as _p:
        # query the default sink
        sink_def = get_sink(pulse=_p)

        # get the starting vol
        start_vol = get_volume_rounded(pulse=_p, sink=sink_def)

        # change the volume
        set_volume(pulse=_p, sink=sink_def, adjustment=change)

        # query the volume again
        new_volume = get_volume_rounded(pulse=_p, sink=sink_def)

        # construct data dict for CLI output/reference
        data['sink'] = sink_def.name
        data['change'] = change
        data['start_vol'] = start_vol
        data['new_vol'] = new_volume

        # Create a desktop notification
        notification_id = notifications.Notify(
            'volume-changer', 0, 'dialog-information', 
            'Volume Change', 
            f"Now {data['new_vol']}%, was {data['start_vol']}%", 
            [], {}, 1000)
except pulsectl.PulseError as e:
    data['sink'] = None
    data['change'] = 'Impossible, exception: {e}'
    # notify that we couldn't work with pulseaudio/compatible daemon
    notification_id = notifications.Notify(
        'volume-changer', 0, 'dialog-error',
        'Volume Change', 
        f"Exception: {e}",
        [], {}, 1000)

print(data, flush=True)
