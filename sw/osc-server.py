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


PANEL_ROTATION =  3
WIDTH = NUM_PANELS * 32
HEIGHT = 32

global then
then = time.perf_counter()

def send_hex_handler(unused_addr, args, frame_data):
    global then
    #print("[{0}] ~ {1}".format(args[0], frame_data))
    
    h.hexframe(frame_data)
    h.sendframe()
    now = time.perf_counter()
    print("delta time: {}".format(now - then))
    then = now
    sys.stdout.flush()
    
def print_volume_handler(unused_addr, args, volume):
    print("[{0}] ~ {1}".format(args[0], volume))


def print_compute_handler(unused_addr, args, volume):
    try:
        print("[{0}] ~ {1}".format(args[0], args[1](volume)))
    except ValueError:
        pass


if __name__ == "__main__":

    print("init ht1632c")
    h=ht1632c.HT1632C(NUM_PANELS, PANEL_ROTATION)


    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=5005, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/filter", print)
    dispatcher.map("/hexframe", send_hex_handler, "Hexframe")
    #dispatcher.map("/volume", print_volume_handler, "Volume")
    #dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
