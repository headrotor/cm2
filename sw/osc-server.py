"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import sys
import argparse
import math
import ht1632c
import time

from pythonosc import dispatcher
from pythonosc import osc_server


NUM_PANELS = 1
# defult to flip vertical and rotate so origin is at top left. 
PANEL_ROTATION = 3
WIDTH = NUM_PANELS * 32
HEIGHT = 32

class OscHandlers(object):
    def __init__(self, client, args):
        self.then = time.perf_counter()
        self.h = client
        self.silent = args.silent
        self.print_rate = args.print_rate
        self.throttle_time = 1./args.throttle_fps    
        self.throttle_then = time.time()
        self.fontdict = {'3x4num':h.font3x4num,   
                         '4x5num':h.font4x5num,  
                         '7x8num':h.font7x8num,  
                         '4x6':h.font4x6,      
                         '5x8':h.font5x8,      
                         '6x8':h.font6x8,      
                         '7x12':h.font7x12,     
                         '8x12':h.font8x12,     
                         '12x16':h.font12x16,    
                         '4x6sym':h.font4x6sym}
        # font to use for next putsr
        self.font = self.fontdict['12x16']

    def print_fps(self):
        # crude estimate of frame rate
        if self.print_rate:
            now = time.perf_counter()
            #print("delta time: {}".format(now - self.then))
            print("fps: {:5.2f}".format(1.0/(now - self.then)))
            self.then = now
            sys.stdout.flush()

    def throttle_block(self):
        # crude frame rate throttling: block until throttle time has passed
        #print(str(time.time() - self.throttle_then))
        while (time.time() - self.throttle_then) < self.throttle_time:
            time.sleep(0.001)
            
    def send_hex(self, unused_addr, args, frame_data):
        self.throttle_block()
        self.h.hexframe(frame_data)
        self.h.sendframe()
        self.throttle_then = time.time()
        self.print_fps()
        
    def draw_line(self, unused_addr, args, data):
        #print("Line handler")
        self.h.line(data[0], data[1], data[2], data[3], 1)
        self.h.sendframe()
        self.throttle_then = time.time()
        self.print_fps()

    def draw_box(self, unused_addr, args, data):
        #print("Line handler")
        self.h.box(data[0], data[1], data[2], data[3], 1)
        self.h.sendframe()
        self.throttle_then = time.time()
        self.print_fps()

    def plot_pixel(self, unused_addr, args, data):
        print("Plot handler")
        self.h.plot(data[0], data[1], data[2])
        self.h.sendframe()
        
    def send_clear(self, unused_addr, args, data):
        #print("Clear")
        h.clear()
        h.sendframe()
    # def print_volume_handler(unused_addr, args, volume):
    #     print("[{0}] ~ {1}".format(args[0], volume))


    def set_bright(self, unused_addr, args, brightness):
        # given an ascii string brightnes value, convert to int and send
        pwm_val = self.check_int_param(brightness,0, 15)
        #if not args.silent:
        print("setting pwm to {}".format(pwm_val))
        self.h.pwm(pwm_val)

    def set_font(self, unused_addr, args, font_name):    
        print(f"setting fornt to {font_name}")
        try:
            self.font = self.fontdict[font_name]
        except KeyError:
            print('Font "{}" not found, try one of')
            for key in self.fontdict:
                print(key)
            self.font = self.fontdict[key]

    def send_text(self,unused_addr, args, data): 
        print(f"setting text to {data}")

        text_str = data[0]
        x = data[1]
        y = data[2]
        self.h.putstr(x, y, text_str, self.font, 1, 0)
        self.h.sendframe()


    def check_int_param(self, param_str, pmin, pmax):
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

def send_hex_handler(unused_addr, args, frame_data):
    global then
    #print("[{0}] ~ {1}".format(args[0], frame_data))
    
    h.hexframe(frame_data)
    h.sendframe()
    now = time.perf_counter()
    #print("delta time: {}".format(now - then))
    then = now
    sys.stdout.flush()



def print_compute_handler(unused_addr, args, volume):
    try:
        print("[{0}] ~ {1}".format(args[0], args[1](volume)))
    except ValueError:
        pass


if __name__ == "__main__":



    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=5005, help="The port to listen on")

    parser.add_argument("--silent",
                        help="don't print anything to stdout",
                        action="store_true")
    parser.add_argument("--print_rate",
                        help="generate crude frame rate measurement",
                        action="store_true")
    parser.add_argument("--throttle_fps",
                        type=int,
                        default=1000,
                        help="Try to throttle frame rate to this (fps)")
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
    if args.swap_xy:
        PANEL_ROTATION = PANEL_ROTATION - 1
    if args.flip_vertical:
        PANEL_ROTATION = PANEL_ROTATION - 2
    if args.flip_horizontal:
        PANEL_ROTATION = PANEL_ROTATION + 4
    h=ht1632c.HT1632C(NUM_PANELS, PANEL_ROTATION)

    handlers = OscHandlers(client=h, args=args)


    dispatcher = dispatcher.Dispatcher()
    dispatcher.client = h
    dispatcher.map("/filter", print)
    dispatcher.map("/hexframe", handlers.send_hex, "Hexframe")
    dispatcher.map("/pixel", handlers.plot_pixel, "Pixel")
    dispatcher.map("/bright", handlers.set_bright, "Brightness")
    dispatcher.map("/line", handlers.draw_line, "Line")
    dispatcher.map("/box", handlers.draw_box, "Box")
    dispatcher.map("/font", handlers.set_font, "Font")
    dispatcher.map("/text", handlers.send_text, "Text")
    dispatcher.map("/clear", handlers.send_clear, "Clear")

    #dispatcher.map("/volume", print_volume_handler, "Volume")
    #dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
