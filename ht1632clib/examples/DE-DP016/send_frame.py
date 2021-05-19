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

print("init ht1632c")
h=ht1632c.HT1632C(NUM_PANELS, PANEL_ROTATION)

h.pwm(15)

pix_w = 8
pix_h = 8
# four bits per hex char
num_chars = pix_h * pix_w / 4
chars_per_col = pix_w / 4

if len(sys.argv) == 2:
    # parse string of hex digits
    hex_frame =  sys.argv[1].strip()
    if len(hex_frame) != (num_chars):
        print("need %d chars in frame data\n" % int(num_chars))
        exit(1)
    
elif len(sys.argv) == 3:
    # handle command
    for c in sys.argv[2]:
        print(c)


m = 0
for i,c in enumerate(hex_frame):
    n = int(c,16) # convert to binary string
    nstr = format(n, '04b')
    for j in range(4): # 4 bits per hex char
        if (nstr[j])  == '1': 
            print('*',end='')
            h.plot(i/2, m, 1)
        else:
            print('.',end='')
            h.plot(i/2, m, 0)
        #print(str((i, i/2,m)))
        m += 1
    if i % chars_per_col:
        print("")
        m = 0
    #h.plot(j,i,1)

h.sendframe()




h.close()
