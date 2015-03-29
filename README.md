thinkpad-yoga-14-scripts
=====================

A collection of scripts and systemd units to restore functionality of
the Lenovo ThinkPad Yoga 14 S3.

These are different from other scripts in that the screen rotation is
automated with use of the inbuilt accelerometer. Also, acpid is not
used in order to toggle between tablet mode but rather binding to the
inbuilt switches.


Tested on Linux Mint with Cinnamon. See customization.

Modified from https://github.com/ianalis/thinkpad-yoga-scripts

# Scripts should fix:

- Screen rotation with accelerometer, including touchscreen geometries,
  and disabling of Touchpad/TrackPoint

  Adjustment of screen brightness

# Usage/Customization:

Assuming installed as per the PKGBUILD

Depending whether or not your DE rotates the touchscreen automatically
edit the following file accordingly:

    /opt/thinkpad-yoga-14-S3/rotate/thinkpad-rotate.py


# TODO:
- Test on different desktop environments (You can help!)

# Dependencies
- xrandr
- xinput
- systemd
- gawk

# Manual installation

    sudo -s
    git clone https://github.com/johanneswilm/thinkpad-yoga-14-s3 /opt/thinkpad-yoga-14-s3
    cp /opt/thinkpad-yoga-14-s3/systemd/* /usr/lib/systemd/system/

    systemctl start yoga-rotate@username.service
    systemctl start yoga-backlight@username.service
