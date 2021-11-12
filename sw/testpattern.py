#!/usr/bin/env python
from __future__ import print_function
# Send one frame to the LED display.
# if one argument, it's a hex string of pixels
# if two args, first arg is ignored (could be '-C'), second arg is command



import os
import sys
#print os.environ
import time
import timeit
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

def send_two_grids():
    # test for framerate: alternately light two top left pixels
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if (i + j) % 2 == 0:
                h.plot(i,j,0)
            else:
                h.plot(i,j,1)
    h.sendframe()
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if (i + j) % 2 == 0:
                h.plot(i,j,1)
            else:
                h.plot(i,j,0)
    h.sendframe()


def send_two_frames():
    # test for framerate: alternately light alternate pixels
    h.plot(0, 0, 1)            
    h.plot(0, 1, 0)            
    h.sendframe()
    h.plot(0, 0, 0)            
    h.plot(0, 1, 1)            
    h.sendframe()

def send_two_hex_frames():
    # test for framerate: alternately light alternate pixels
    h.hexframe('F0000000800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001FFFFFFFF')
    h.sendframe()

    h.hexframe('FFFFFFFF800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001FFFFFFFF')
    h.sendframe()

    

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
        elif mode == "time":
            h.clear()
            #send_time = timeit.timeit(h.sendframe,number=100)
            repeat_count = 10
            #send_time = timeit.timeit(send_two_frames,number=repeat_count)
            send_time = timeit.timeit(send_two_hex_frames,number=repeat_count)
            # seconds per frame (spf) is send_time/number of frames so
            # fps is 1/spf = repeat_count * 2 / send_time
            fps = 2.*repeat_count/send_time
            print("sendframe rate: {:6.1f} fps (reps = {})".format(fps, repeat_count))

        elif mode == "bright":
            h.pwm(0)
            send_two_grids()
            for i in range(15):
                # fade up from pwm 0
                print("Set PWM to {}/15".format(i))
                h.pwm(i)
                time.sleep(0.2)
            for i in range(14):
                # fade down from PWM 15
                #send_time = timeit.timeit(h.sendframe,number=100)
                print("Set PWM to {}/15".format(15-i))
                h.pwm(15-i)
                time.sleep(0.2)

        elif mode == "hex":
            print('Clearing display. Bye.')
            h.hexframe('F0000000800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001FFFFFFFF')
            h.sendframe()
            h.close()
            sys.exit()
        elif mode == "clear":
            print('Clearing display. Bye.')
            h.clear()
            h.close()
            sys.exit()
        else:
            print('unrecognized mode "{}"'.format(mode))
            h.close()
            sys.exit()

except KeyboardInterrupt:
    # quit
    print("\nbye!")
    h.close()
    sys.exit()

