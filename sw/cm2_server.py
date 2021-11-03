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

def send_hex(hex_frame):
    # send a frame of hexidecimal data to the cm2 display
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

      fields = urlparse.urlparse(self.path)
      #print(self.path)
      print(fields)
      hex_frame = fields[4]
      send_hex(str(hex_frame))
      print_hex(str(hex_frame))
      SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
      
Handler = ServerHandler

#server = MyTCPServer(('0.0.0.0', 8080), Handler)

#httpd = MyTCPServer.TCPServer(("", PORT), Handler)
SocketServer.TCPServer.allow_reuse_address = True
httpd = SocketServer.TCPServer(("", PORT), Handler)


print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.shutdown()
    h.close()
    exit()
