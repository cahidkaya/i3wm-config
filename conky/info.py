#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import sys

import argparse
parser = argparse.ArgumentParser(description='Provides some useful infos about the system.')

parser.add_argument('--battery', action='store_true', help="show battery infos")
parser.add_argument('--get-brightness',
                    action='store_true',
                    dest='get_brightness',
                    help="show brightness infos")
parser.add_argument('--set-brightness',
                    action='store',
                    type=int,
                    dest='set_brightness',
                    help="set brightness")

args = parser.parse_args()

if args.battery:
    p = subprocess.Popen('acpi -b', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for line in p.stdout.readlines():
        name, infos = line.split(': ')
        status, percentage, eta = infos.split(', ')
        eta = eta[:8]
        status_sym = status == 'Charging' and '↗' or '↘'
        sys.stdout.write('⚡: %s (%s %s)\n' % (percentage, status_sym, eta))
    #retval = p.wait()

elif args.get_brightness:
    command_current_b = 'pkexec /usr/lib/gnome-settings-daemon/gsd-backlight-helper --get-brightness'
    command_max_b = 'pkexec /usr/lib/gnome-settings-daemon/gsd-backlight-helper --get-max-brightness'

    p = subprocess.Popen(command_current_b, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    current_b = int(p.stdout.readlines()[0].replace('\n', ''))
    p = subprocess.Popen(command_max_b, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    max_b = int(p.stdout.readlines()[0].replace('\n', ''))
    percentage = current_b * 100 / max_b
    sys.stdout.write('☀: %s%%\n' % percentage)
elif args.set_brightness:
    new_b = int(args.set_brightness)
    command = 'pkexec /usr/lib/gnome-settings-daemon/gsd-backlight-helper --set-brightness %s'
    p = subprocess.Popen(command % new_b, shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
else:
    parser.print_help()
