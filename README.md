thinkpad-yoga-rotate
====================

A small utility script to automatically rotate the screen of Thinkpad Yoga in Linux, when switching to or from the tablet mode. Relies on acpid and xrandr. 

The Arch Linux package is in the subfolder, and also available on AUR as thinkpad-yoga-rotate. You need to restart acpid after installing the package.

For non-Arch users:
  - copy `tablet-mode` into `/etc/acpi/events`
  - copy `rotate-screen.py` into `/etc/acpi/actions` and make it executable (`chmod +x /etc/acpi/actions/rotate-screen.py`)
  - restart acpid
