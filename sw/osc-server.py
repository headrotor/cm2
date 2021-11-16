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

global then
then = time.perf_counter()

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

def send_hex_handler(unused_addr, args, frame_data):
    global then
    #print("[{0}] ~ {1}".format(args[0], frame_data))
    
    h.hexframe(frame_data)
    h.sendframe()
    now = time.perf_counter()
    print("delta time: {}".format(now - then))
    then = now
    sys.stdout.flush()
    
# def print_volume_handler(unused_addr, args, volume):
#     print("[{0}] ~ {1}".format(args[0], volume))

def brightness_handler(brightness_str):
    # given an ascii string brightnes value, convert to int and send
    pwm_val = check_int_param(brightness_str,0, 15)
    if not args.silent:
        print("setting pwm to {}".format(pwm_val))
    h.pwm(pwm_val)



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



    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/filter", print)
    dispatcher.map("/hexframe", send_hex_handler, "Hexframe")

    #dispatcher.map("/volume", print_volume_handler, "Volume")
    #dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
