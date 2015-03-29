#!/usr/bin/env python

import glob
import os.path
import sys
import math
import time

# min value of light sensor for automatic adjustment of backlight
LS_LOW = 1
# max value of light sensor for automatic adjustment of backlight
LS_HIGH = 500
# scale factor of backlight value exponential function
SCALE = 89
# exponent scaling factor of backlight exponential function
EXP = 0.004615
# minimum change in sensor intensity before backlight intensity is changed
TOL = 5
# time in seconds between successive sensor reads
SLEEP_TIME = 1

sensor_dir = None
for f in glob.glob('/sys/bus/iio/devices/iio:device*/name'):
    if 'als' in open(f).read():
        sensor_dir = os.path.dirname(f)
if not sensor_dir:
    print('sensor not found')
    sys.exit(-1)

abs_max_bl = int(open('/sys/class/backlight/intel_backlight/'
                      'max_brightness').read())
min_bl = max(int(SCALE * math.exp(EXP * LS_LOW)), 0)
max_bl = min(int(SCALE * math.exp(EXP * LS_HIGH)), abs_max_bl)

old_bl_val = -100
while 1:
    with open(os.path.join(sensor_dir, 'in_intensity_both_raw')) as ls_file:
        ls_val = int(ls_file.readline().strip())

    if ls_val < LS_LOW:
        bl_val = min_bl
    elif LS_LOW <= ls_val < LS_HIGH:
        bl_val = int(SCALE * math.exp(EXP * ls_val))
        bl_val = max(bl_val, min_bl)
        bl_val = min(bl_val, max_bl)
    else:
        bl_val = max_bl
    
    if abs(bl_val - old_bl_val) >= TOL:
        with open('/sys/class/backlight/intel_backlight/brightness', 'w') as bl_file:
            bl_file.write('%s\n' % (bl_val))
        print min_bl, max_bl, ls_val, bl_val

    old_bl_val = bl_val
    time.sleep(SLEEP_TIME)
