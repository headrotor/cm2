"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import time
import timeit

from pythonosc import osc_message_builder
from pythonosc import udp_client


def send_two_hex_frames(client, delay):

    # test for framerate: alternately light alternate pixels
    frame1 = "aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555"

    frame2 = "55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa"
    client.send_message("/hexframe", frame1)
    time.sleep(delay)
    client.send_message("/hexframe", frame2)
    time.sleep(delay)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1",
                        help="The ip of the OSC server")
    parser.add_argument("--port",
                        type=int,
                        default=5005,
                        help="The port the OSC server is listening on")
    parser.add_argument("--brightness",
                        type=int,
                        help="PWM brightness 0-15")
    parser.add_argument("--fps",
                        type=int,
                        default=30,
                        help="Frames per second")
    parser.add_argument('mode')
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    # sleep for this many seconds between frames
    frametime = 1./float(args.fps)

    if args.brightness is not None:
        print(f"Setting brightness to {args.brightness}")
        client.send_message("/bright", args.brightness)
    
    if args.mode == 'time':

        while True:
            try:
                repeat_count = 100
                #send_time = timeit.timeit(send_two_frames,number=repeat_count)
                send_time = timeit.timeit(
                    "send_two_hex_frames(client, frametime)",
                    setup="from __main__ import send_two_hex_frames, client, frametime",
                    number=repeat_count)
                # seconds per frame (spf) is send_time/number of frames so
                # fps is 1/spf = repeat_count * 2 / send_time
                fps = 2. * repeat_count / send_time
                print("sendframe rate: {:6.1f} fps (reps = {})".format(
                    fps, repeat_count))
            except KeyboardInterrupt:
                break
            
    elif args.mode == 'line':
        print("sending lines")
        while True:
            try:
                for i in range(32):
                    client.send_message("/clear", True)
                    client.send_message("/line", [[0,i,31,31-i]])
                    time.sleep(frametime)
                for j in range(32):
                    client.send_message("/clear", True)
                    client.send_message("/line", [[31-j,0,j,31]])
                    time.sleep(frametime)
            except KeyboardInterrupt:
                break

    elif args.mode == 'box':
        print("sending lines")
        while True:
            try:
                client.send_message("/clear", True)
                for i in range(32):
                    client.send_message("/box", [[0,0,i,i]])
                    time.sleep(frametime)
            except KeyboardInterrupt:
                break
        


    elif args.mode == 'text':
        print("sending text")
        while True:
            try:
                for i in range(180):
                    client.send_message("/clear", True)
                    client.send_message("/text", [['Hello world!',5-i,10]])
                    time.sleep(frametime)
            except KeyboardInterrupt:
                break

    elif args.mode == 'font':
        print("setting font")
        client.send_message("/font", ['7x12'])
        
    elif args.mode == 'clear':
        print("sending clear")
        client.send_message("/clear", True)
        
    else:
        print("unrecognized mode: " + args.mode)
