#!/usr/bin/env python3
"""
thinkpad-rotate.py

Rotates any detected screen, wacom digitizers, touchscreens,
touchpad/trackpoint based on orientation gathered from accelerometer.

Tested with Lenovo Thinkpad 14 Yoga S3

https://github.com/johanneswilm/thinkpad-yoga-14-s3-scripts

Acknowledgements:
Modified from source:
https://gist.githubusercontent.com/ei-grad/4d9d23b1463a99d24a8d/raw/rotate.py

"""

### BEGIN Configurables

rotate_pens = True # Set false if your DE rotates pen for you
disable_touchpads = True

### END Configurables


from time import sleep
from os import path as op
import sys
from subprocess import check_call, check_output
from glob import glob
from os import environ

def bdopen(fname):
    return open(op.join(basedir, fname))


def read(fname):
    return bdopen(fname).read()


for basedir in glob('/sys/bus/iio/devices/iio:device*'):
    if 'accel' in read('name'):
        break
else:
    sys.stderr.write("Can't find an accellerator device!\n")
    sys.exit(1)


env = environ.copy()

devices = check_output(['xinput', '--list', '--name-only'],env=env).splitlines()
touchscreen_names = ['touchscreen', 'touch digitizer', 'finger']
touchscreens = [i.decode('utf-8') for i in devices if any(j in i.lower().decode('utf-8') for j in touchscreen_names)]

wacoms = [i.decode('utf-8') for i in devices if any(j in i.lower().decode('utf-8') for j in ['pen stylus', 'pen eraser'])]

touchpad_names = ['touchpad', 'trackpoint', 'stick']
touchpads = [i.decode('utf-8') for i in devices if any(j in i.lower().decode('utf-8') for j in touchpad_names)]

scale = float(read('in_accel_scale'))

g = 7.0  # (m^2 / s) sensibility, gravity trigger

STATES = [
    {'rot': 'normal', 'pen': 'none', 'coord': '1 0 0 0 1 0 0 0 1', 'touchpad': 'enable',
     'check': lambda x, y: y <= -g},
    {'rot': 'inverted', 'pen': 'half', 'coord': '-1 0 1 0 -1 1 0 0 1', 'touchpad': 'disable',
     'check': lambda x, y: y >= g},
    {'rot': 'left', 'pen': 'ccw', 'coord': '0 -1 1 1 0 0 0 0 1', 'touchpad': 'disable',
     'check': lambda x, y: x >= g},
    {'rot': 'right', 'pen': 'cw', 'coord': '0 1 0 -1 0 1 0 0 1', 'touchpad': 'disable',
     'check': lambda x, y: x <= -g},
]


def rotate(state):
    s = STATES[state]
    check_call(['xrandr', '-o', s['rot']],env=env)
    for dev in touchscreens if disable_touchpads else (touchscreens + touchpads):
        check_call([
            'xinput', 'set-prop', dev,
            'Coordinate Transformation Matrix',
        ] + s['coord'].split(),env=env)
    if rotate_pens:
        for dev in wacoms:
            #print('xsetwacom','set', "'"+dev+"'",'rotate',s['pen']) # debug
            check_call([
                'xsetwacom','set',dev,
                'Rotate',s['pen']],env=env)
    if disable_touchpads:
        for dev in touchpads:
            check_call(['xinput', s['touchpad'], dev],env=env)

def read_accel(fp):
    fp.seek(0)
    return float(fp.read()) * scale


if __name__ == '__main__':

    accel_x = bdopen('in_accel_x_raw')
    accel_y = bdopen('in_accel_y_raw')

    current_state = None

    while True:
        x = read_accel(accel_x)
        y = read_accel(accel_y)
        for i in range(4):
            if i == current_state:
                continue
            if STATES[i]['check'](x, y):
                current_state = i
                #print(i) # debug
                rotate(i)
                break
        sleep(1)
