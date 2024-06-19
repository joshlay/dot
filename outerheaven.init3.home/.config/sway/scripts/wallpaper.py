#!/usr/bin/env python3
"""
wallpaper.py - random wallpaper/output utility for i3/Sway

usage: wallpaper.py [-h] [--select {common,unique}] directory

Selection modes:
    Common: One wallpaper selected and shared for *all* displays
    Unique: One wallpaper selected for *each* display
"""
import argparse
import os
import sys
import random
import asyncio
from typing import List
from i3ipc.aio import Connection

EXTS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

def parse_args():
    '''Handles argparse on startup'''
    parser = argparse.ArgumentParser(description='Random Wallpaper Setter for Sway')
    parser.add_argument('directory', type=str, help='Directory containing wallpapers')
    parser.add_argument('--select',
                        type=str,
                        choices=['common', 'unique'],
                        default='common',
                        help='Wallpaper selection mode: all displays, or each?')
    return parser.parse_args()

async def main():
    '''you know what it is'''
    args = parse_args()
    sway = await Connection(auto_reconnect=True).connect()
    def list_image_files(d: str) -> List[str]:
        '''
        Given the path to a *'directory'*, returns a list of image files to consider for wallpapers.
        '''
        return [os.path.join(d, f) for f in os.listdir(d) if os.path.splitext(f)[1].lower() in EXTS]

    async def set_wallpaper(file_path: str, output=None):
        '''
        Given an image path, sets the wallpaper for (optional) outputs in i3/Sway.

        If no output is specified then *all* will receive the wallpaper.
        '''
        print(f"{output if output else 'all'}: wallpaper='{file_path}'")
        if output:
            await sway.command(f'output "{output}" bg "{file_path}" fill')
        else:
            for _output in await sway.get_outputs():
                await sway.command(f'output "{_output.name}" bg "{file_path}" fill')

    if os.path.isdir(args.directory):
        image_files = list_image_files(args.directory)
    else:
        sys.exit(f'ERR: not a directory: {args.directory}')
    if not image_files:
        print("No image files found in the specified directory.")
        return

    print(f'Found {len(image_files)} candidate image files')
    outputs = await sway.get_outputs()

    if args.select == 'common':
        wallpaper = random.choice(image_files)
        await set_wallpaper(wallpaper)
    else:  # args.select == 'unique', we need to determine a wallpaper for each display
        for output in outputs:
            if len(image_files) == 0:
                print(f"Not enough images in '{args.directory}' for each display.")
                break
            wallpaper = random.choice(image_files)
            image_files.remove(wallpaper)
            await set_wallpaper(wallpaper, output.name)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
