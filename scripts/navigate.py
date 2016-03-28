#!/usr/bin/env python

import os
import argparse
import subprocess

parser = argparse.ArgumentParser(
    description='Sends set_destination command to Navit using dbus-send')
parser.add_argument('lng', type=float, help='Destination longitude')
parser.add_argument('lat', type=float, help='Destination latitude')
parser.add_argument('title', type=str, default='', help='Title of the place')

args = parser.parse_args()

command = [
    '/usr/bin/dbus-send',
    '--print-reply',
    '--session',
    '--dest=org.navit_project.navit',
    '/org/navit_project/navit/default_navit',
    'org.navit_project.navit.navit.set_destination',
    'string:"geo:%s %s" string:"%s"' % (args.lng, args.lat, args.title)
]

command = ' '.join(command)

os.environ["DISPLAY"] = ":0"

try:
    output = subprocess.check_output(
        command, shell=True, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError as e:
    pass
