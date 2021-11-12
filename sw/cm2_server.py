#!/usr/bin/env python

# This is Python 2, for default use with rpi.
# As of 2021 that's what we have. Ssorry!

from __future__ import print_function
from __future__ import division
# adapted form https://gist.github.com/kylemcdonald/3bb71e4b901c54073cbc

import SimpleHTTPServer
import SocketServer
import urlparse
import argparse

# Send one frame to the LED display.

import os
import sys
#print os.environ
import time
import ht1632c

           
PORT = 8000


NUM_PANELS = 1
WIDTH = NUM_PANELS * 32
HEIGHT = 32



parser = argparse.ArgumentParser()


parser.add_argument("--silent",
                    help="don't print anything to stdout",
                    action="store_true")
parser.add_argument("--simulate",
                    help="print a simulated screen to stdout",
                    action="store_true")
parser.add_argument("--flip_horizontal",
                    help="reverse horizontal direction, x=0 is at right",
                    action="store_true")
parser.add_argument("--swap_xy",
                    help="swap x and y directions, y is horizontal, x is vertical",
                    action="store_true")
parser.add_argument("--flip_vertical",
                    help="reverse vertical direction, y=0 is at bottom",
                    action="store_true")

args = parser.parse_args()
print("init ht1632c")


# defult to flip vertical and rotate so origin is at top left. 
PANEL_ROTATION = 3

if args.swap_xy:
    PANEL_ROTATION = PANEL_ROTATION - 1


if args.flip_vertical:
    PANEL_ROTATION = PANEL_ROTATION - 2

if args.flip_horizontal:
    PANEL_ROTATION = PANEL_ROTATION + 4


h=ht1632c.HT1632C(NUM_PANELS, PANEL_ROTATION)

h.pwm(15)

pix_w = 32
pix_h = 32
# four bits per hex char
num_chars = pix_h * pix_w // 4
chars_per_col = pix_w // 4



def check_int_param(param_str, pmin, pmax):
    # given an ascii string param, convert to int and check value
    try:
        param_int = int(param_str)
    except ValueError:
        print('Error converting "{}" to int'.format(param_str))
        return pmin

    if param_int < pmin:
        return pmin
    if param_int > pmax:
        return pmax
    return param_int
    
def set_brightness(brightness_str):
    # given an ascii string brightnes value, convert to int and send
    pwm_val = check_int_param(brightness_str,0, 15)
    if not args.silent:
        print("setting pwm to {}".format(pwm_val))
    h.pwm(pwm_val)

    
def send_hex(hex_frame):
    m = 0
    for i,c in enumerate(hex_frame):
        n = int(c,16) # convert to binary string
        nstr = format(n, '04b')
        col = i // chars_per_col
        for j in range(4): # 4 bits per hex char
            if (nstr[j])  == '1': 
                h.plot(col, m, 1)
            else:
                h.plot(col, m, 0)
            m += 1
        if m >=  pix_h:
            m = 0
    h.sendframe()

def send_hex_old(hex_frame):
    # old slow version, decode hex and set bit-by-bit
    m = 0
    for i,c in enumerate(hex_frame):
        n = int(c,16) # convert to binary string
        nstr = format(n, '04b')
        col = i // chars_per_col
        for j in range(4): # 4 bits per hex char
            if (nstr[j])  == '1': 
                h.plot(col, m, 1)
            else:
                h.plot(col, m, 0)
            m += 1
        if m >=  pix_h:
            m = 0
    h.sendframe()

def send_hex(hex_frame_data):
    # new fast version, send entire frame to driver
    h.hexframe(hex_frame_data)
    h.sendframe()

    
def send_text(text_str, x=0, y=0, font_name='7x8num', clear = False):
    fontdict = {'3x4num':h.font3x4num,   
                '4x5num':h.font4x5num,  
                '7x8num':h.font7x8num,  
                '4x6':h.font4x6,      
                '5x8':h.font5x8,      
                '6x8':h.font6x8,      
                '7x12':h.font7x12,     
                '8x12':h.font8x12,     
                '12x16':h.font12x16,    
                '4x6sym':h.font4x6sym}  

    try:
        font = fontdict[font_name]
    except KeyError:
        print('Font "{}" not found, try one of')
        for key in fontdict:
            print(key)
        font = fontdict['12x16']
            
    if clear:
        h.clear()
    h.putstr(x, y, text_str, font, 1, 0)

    h.sendframe()

def print_hex(hex_frame):
    # for debugging, send ascii frame to stdout
    m = 0
    for i,c in enumerate(hex_frame):
        n = int(c,16) # convert to binary string
        nstr = format(n, '04b')
        col = i // chars_per_col
        #print(nstr)
        for j in range(4): # 4 bits per hex char
            if (nstr[j])  == '1': 
                print('* ',end='')
            else:
                print('- ',end='')
            m += 1
        if m >=  pix_h:
            # end of line, print newline
            print("")
            m = 0

class MyTCPServer(SocketServer.TCPServer):
    def __init__(self, serverAddress, handler):
        super().__init__(serverAddress, handler)
        self.allow_reuse_address = True



class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def __init__(self, *args):
        self.font_name = '12x16'
        SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, *args)

    #quiet log messages    
    def log_message(self, format, *args):
        return

        
    def do_GET(self):
        #content_len = int(self.headers.getheader('content-length', 0))
        #post_body = self.rfile.read(content_len)

        # parse URL into fields
        parsed = urlparse.urlparse(self.path)

        # extract query paramaters as dict
        qdict = urlparse.parse_qs(parsed.query)
        if not args.silent:
            print(str(qdict))

        # default parameters
        x = 0
        y = 0
        clear = False
        
        # respond to each query paramater
        for key in  qdict:
            #print("Got key " + key)
            if key == 'frame':
                hex_frame = qdict[key][0] 
                send_hex(hex_frame)
                if args.simulate:
                    print_hex(hex_frame)
            elif key == 'clear':
                clear = True
            elif key == 'bright':
                bright_str = qdict[key][0] 
                set_brightness(bright_str)
            elif key == 'text':
                text_str = qdict[key][0] 
                send_text(text_str, x, y, self.font_name, clear)
                if not args.silent:
                    print('setting text "{}"'.format(text_str))
            elif key == 'font':
                self.font_name = qdict[key][0] 
                if not args.silent:
                    print('setting font to "{}"'.format(self.font_name))

            elif key == 'x':
                param_str = qdict[key][0] 
                try:
                    x = int(param_str)
                except ValueError:
                    print('Error converting "{}" to int'.format(param_str))
                    break
            elif key == 'y':
                param_str = qdict[key][0] 
                try:
                    y = int(param_str)
                except ValueError:
                    print('Error converting "{}" to int'.format(param_str))
                    break

            else:
                print('Unrecognized parameter "{}", ignoring'.format(key))

                
        #SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        self.send_response(200)

Handler = ServerHandler

#server = MyTCPServer(('0.0.0.0', 8080), Handler)

#httpd = MyTCPServer.TCPServer(("", PORT), Handler)
SocketServer.TCPServer.allow_reuse_address = True
httpd = SocketServer.TCPServer(("", PORT), Handler)




if not args.silent:
    print("CM2 server listening at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.shutdown()
    h.close()
    exit()
