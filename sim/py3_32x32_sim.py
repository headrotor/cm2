#!/usr/bin/env python
# This is python3 
# Simple server to simulate LED panel display.
#
# Usage: send a GET request to the http:/ip:port url this server is running on,
# followed by "data?"  then a 256-char hex string. Each hex digit
# represents 4 LED bits in row-major order, each of the 32 rows is
# represented by 8 succesive hex digits.  Example: this will draw a box around the display
#
# curl -s http://127.0.0.1:8000/data?FFFFFFFF800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001FFFFFFFF
#
# other methods:
#
# /display: turn display on or off, zero for off, nonzero int to turn on
# curl -s http://127.0.0.1:8000/display?0
#
# /bright: set brightness, integer 0-15
# curl -s http://127.0.0.1:8000/bright:15
#
# adapted from https://gist.github.com/kylemcdonald/3bb71e4b901c54073cbc


import http.server
import socketserver
import urllib.parse
import os
import sys

# serve on this port
PORT = 8000


pix_w = 32
pix_h = 32
# four bits per hex char
num_chars = pix_h * pix_w // 4
chars_per_col = pix_w // 4

def print_hex(hex_frame):
    '''given hex representation of LED frame, print an ascii representation'''
    row = 0
    for i,c in enumerate(hex_frame):
        n = int(c,16) # convert to binary string
        nstr = format(n, '04b')
        col = i // chars_per_col
        #print(nstr)
        for j in range(4): # 4 bits per hex char
            if (nstr[j])  == '1': 
                print('* ',end='')
                #h.plot(col, row, 1)
            else:
                print('- ',end='')
                #h.plot(col, row, 0)
            #print(str((i, col,row)))
            row += 1
        if row >=  pix_h:
            print("")
            row = 0

class ServerHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
      #content_len = int(self.headers.getheader('content-length', 0))
      #post_body = self.rfile.read(content_len)

      (s, n, path, p, query, f) = urllib.parse.urlparse(self.path)
      #print("path is " + path)
      #print("query is " + query)


      if path == '/data':
          if len(query) >= 256:
              print_hex(str(query))
      elif path == '/bright':
          # set brightness, integer 0-15
          pwm = int(query)
          # test for range 0-15 here
          print("set brightness to {}/15".format(pwm)) 
      elif path == '/display':
          # turn display on or off, nonzero int to turn on
          off = (int(query) == 0)
          if off:
              print("display set to OFF")
          else:
              print("display set to ON")
      elif path == '/glow':
          # Experimental:turn background glow on or off, nonzero int to turn on
          # glow can't be turned off if display is on
          off = (int(query) == 0)
          if off:
              print("glow set to OFF")
          else:
              print("glow set to ON")
      else:
          http.server.SimpleHTTPRequestHandler.do_GET(self)
      
Handler = ServerHandler
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("", PORT), Handler)


print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.shutdown()
    exit()
