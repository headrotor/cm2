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

#PANEL_ROTATION = 1 + 4
PANEL_ROTATION =  3
WIDTH = NUM_PANELS * 32
HEIGHT = 32


#print "init rotenc"
#r=rotenc.RotEnc(ROTENC_PIN_0, ROTENC_PIN_1, ROTENC_PIN_BTN, rtcallback)

print("init ht1632c")
h=ht1632c.HT1632C(NUM_PANELS, PANEL_ROTATION)

h.pwm(4)

sleeptime=0.1

mode = "default"
if len(sys.argv) > 1:
    mode = sys.argv[1]

print("test pattern mode " + mode)
h.clear()
try:

    while True:
        if mode == "default":
            for i in range(HEIGHT):
                for j in range(WIDTH):
                #for j in range(7):
                    print("h.plot({},{})".format(i,j))
                    #h.plot(HEIGHT-1-j, i, 1)            
                    h.plot(j, i, 1)            
                    h.sendframe()
                    #h.sendframe()
                    time.sleep(sleeptime)
            print("sent on")
            h.clear()
        elif mode == "blink":
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    h.plot(i, j, 0)            
            print("sent off")
            h.sendframe()
            time.sleep(0.5)
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    h.plot(j, i, 1)
            print("sent off")
            h.sendframe()
            time.sleep(0.5)
        elif mode == "squares":
            for j in range(HEIGHT):
                #for j in range(WIDTH):

                #h.clear()
                h.line(0, 0, 0, j,1)
                h.line(0, 0, j, 0,1)
                h.line(0, j, j, j,1)
                h.line(j, 0, j, j,1)
                h.sendframe()
                print("j: " + str(j))
                time.sleep(0.1)
            h.clear()
        elif mode == "text":
            h.clear()
            for j in range(150):

                h.putstr(32-j, 10, "Hello world!", h.font12x16, 1, 0)
                h.sendframe()
                time.sleep(0.1)
                h.clear()

except KeyboardInterrupt:
    # quit
    print("\nbye!")
    h.close()
    sys.exit()

