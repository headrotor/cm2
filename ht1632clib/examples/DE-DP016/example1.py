#!/usr/bin/env python

# Simple example for SURE electronics 32x16 bicolor led dot matrix.
# All led's will be switched on in red, then green, then orange and
# finally turned off (black that is).

import os
#print os.environ
import time
import ht1632c


NUM_PANELS = 1
PANEL_ROTATION = 0
WIDTH = NUM_PANELS * 24
HEIGHT = 16

ROTENC_PIN_0 = 3
ROTENC_PIN_1 = 4
ROTENC_PIN_BTN = 2

BLACK       = 0
GREEN       = 1
RED         =  2
ORANGE      = 3
TRANSPARENT = 0xff

#print "init rotenc"
#r=rotenc.RotEnc(ROTENC_PIN_0, ROTENC_PIN_1, ROTENC_PIN_BTN, rtcallback)

print "init ht1632c"
h=ht1632c.HT1632C(NUM_PANELS, PANEL_ROTATION)

h.pwm(15)

for i in range(8):
    for j in range(2):
        h.plot(j,i,1)

h.sendframe()



time.sleep(1)
print "all led's in red"
h.box(0, 0, WIDTH - 1, HEIGHT - 1, 1)
h.sendframe()
time.sleep(1)
print "off."

h.box(0, 0, WIDTH - 1, HEIGHT - 1, 0)
h.sendframe()
h.close()
