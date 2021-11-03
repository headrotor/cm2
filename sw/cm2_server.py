#!/usr/bin/env python

# This is Python 2, for default use with rpi.
# As of 2021 that's what we have. Ssorry!

from __future__ import print_function
from __future__ import division
# adapted form https://gist.github.com/kylemcdonald/3bb71e4b901c54073cbc

import SimpleHTTPServer
import SocketServer
import urlparse

# Send one frame to the LED display.

import os
import sys
#print os.environ
import time
import ht1632c


PORT = 8000


NUM_PANELS = 1
PANEL_ROTATION = 3
WIDTH = NUM_PANELS * 32
HEIGHT = 32


print("init ht1632c")

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
    print("setting pwm to {}".format(pwm_val))
    h.pwm(pwm_val)

    
def send_hex(hex_frame):
    m = 0
    for i,c in enumerate(hex_frame):
        n = int(c,16) # convert to binary string
        nstr = format(n, '04b')
        col = i // chars_per_col
        #print(nstr)
        for j in range(4): # 4 bits per hex char
            if (nstr[j])  == '1': 
                print('* ',end='')
                h.plot(col, m, 1)
            else:
                print('- ',end='')
                h.plot(col, m, 0)
            #print(str((i, col,m)))
            m += 1
        if m >=  pix_h:
            print("")
            m = 0
        #h.plot(j,i,1)

    h.sendframe()

    
def send_text(text_str, x=0, y=0):
    h.clear()
    h.putstr(x, y, text_str, h.font12x16, 1, 0)
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

    def do_GET(self):
        #content_len = int(self.headers.getheader('content-length', 0))
        #post_body = self.rfile.read(content_len)

        # parse URL into fields
        parsed = urlparse.urlparse(self.path)

        # extract query paramaters as dict
        qdict = urlparse.parse_qs(parsed.query)
        print(str(qdict))

        # default parameters
        x = 0
        y = 0
        
        # respond to each query paramater
        for key in  qdict:
            print("Got key " + key)
            if key == 'frame':
                hex_frame = qdict[key][0] 
                send_hex(hex_frame)
                print_hex(hex_frame)
            elif key == 'bright':
                bright_str = qdict[key][0] 
                set_brightness(bright_str)
            elif key == 'text':
                text_str = qdict[key][0] 
                send_text(text_str, x, y)
                print('setting text "{}"'.format(text_str))

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


print("CM2 server listening at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.shutdown()
    h.close()
    exit()
