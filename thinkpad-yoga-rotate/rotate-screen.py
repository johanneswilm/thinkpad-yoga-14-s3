#!/usr/bin/python

from os import popen
from itertools import chain

TOUCHPAD = 'AlpsPS/2 ALPS DualPoint TouchPad'
TRACKPOINT = 'DualPoint Stick'
TOUCHSCREEN = 'SYNAPTICS Synaptics Touch Digitizer V04'

TS_MATRIX = {
    'normal': [[1, 0, 0],
               [0, 1, 0],
               [0, 0, 1]],
    'left': [[0, -1, 1],
             [1, 0, 0],
             [0, 0, 1]],
}



# Note: xrandr needs to execute in the context of the X server

# Find the user running the X server
user=popen("who -u | grep -F '(:0)' | head -n 1 | awk '{print $1}'").read().split('\n')[0]

# As the same ACPI event is currently emitted for both going in and out
# of the tablet mode, we need to toggle the orientation


# Figure out the current rotation:
current=popen('DISPLAY=:0 su -c "$(printf "xrandr -q --verbose")" '+user+'|grep eDP1|grep -o -E "left|normal"|head -1').read().split('\n')[0]

if current == "normal":
    orientation = "left"
    popen('DISPLAY=:0 su -c "xinput disable \''+TOUCHPAD+'\'" '+user)
    popen('DISPLAY=:0 su -c "xinput disable \''+TRACKPOINT+'\'" '+user)
else:
    orientation = "normal"
    popen('DISPLAY=:0 su -c "xinput enable \''+TOUCHPAD+'\'" '+user)
    popen('DISPLAY=:0 su -c "xinput enable \''+TRACKPOINT+'\'" '+user)

popen('DISPLAY=:0 su -c "xinput set-prop \''+TOUCHSCREEN+'\' \'Coordinate Transformation Matrix\' '+' '.join([str(c) for c in chain(*TS_MATRIX[orientation])])+'" '+user)

popen('DISPLAY=:0 su -c "xrandr -o '+orientation+'" '+user)
