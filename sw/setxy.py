#!/usr/bin/env python
from __future__ import print_function
# Send one frame to the LED display.
# if one argument, it's a hex string of pixels
# if two args, first arg is ignored (could be '-C'), second arg is command



import os
import sys
#print os.environ
import time
import ht1632c



NUM_PANELS = 1

PANEL_ROTATION = 1 + 4
WIDTH = NUM_PANELS * 32
HEIGHT = 32


#print "init rotenc"
#r=rotenc.RotEnc(ROTENC_PIN_0, ROTENC_PIN_1, ROTENC_PIN_BTN, rtcallback)

print("init ht1632c")
h=ht1632c.HT1632C(NUM_PANELS, 0)

h.pwm(4)

sleeptime=0.1

mode = "default"
if len(sys.argv) > 2:
    i = int(sys.argv[1])
    j = int(sys.argv[2])

print("test pattern mode " + mode)
h.clear()
print("h.plot({},{})".format(i,j))
h.plot(i, j, 1)            
h.sendframe()
print("\nbye!")
h.close()
sys.exit()

