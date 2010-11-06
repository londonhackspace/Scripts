#!/usr/bin/env python
import serial, sys, tty, termios, urllib2

print "\nCamera control"
print "--------------\n"
print " Arrow keys move the camera\n"
print " c - center"
print " p - pan scan"
print " t - tilt scan"
print "\nDuring scan, hit any arrow key to stop."

fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
try:
    tty.setraw(sys.stdin.fileno())
    while True:
        ch = ord(sys.stdin.read(1))
        if ch == 3:
            sys.exit()

        cmd = ''
        if ch == 65:
            cmd = 290004
        elif ch == 66:
            cmd = 290003
        elif ch == 68:
            cmd = 290002
        elif ch == 67:
            cmd = 290001
        elif ch == 99:
            cmd = 290301 # Center
        elif ch == 112:
            cmd = 290404 # Pan Scan
        elif ch == 116:
            cmd = 290405 # Tilt Scan
        
        urllib2.urlopen('http://172.31.24.122/cmmd=%s' % cmd);

finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

ser.close()

