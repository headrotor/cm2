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


def send_two_hex_frames(client):

    delay = 0.01  # 100 fps
    # test for framerate: alternately light alternate pixels
    frame1 = "aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555"

    frame2 = "55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa"
    client.send_message("/hexframe", frame1)
    time.sleep(delay)
    client.send_message("/hexframe", frame2)
    time.sleep(delay)

def set_brightness(client, brightness):

    delay = 0.01  # 100 fps
    # test for framerate: alternately light alternate pixels
    client.send_message("/bright", brightness)



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
                        default=15,
                        help="PWM brightness 0-15")
    parser.add_argument('mode')
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)


    if args.brightness is not None:
        print("Set brightness")
        set_brightness(client, args.brightness)
    
    if args.mode == 'time':

        while True:
            try:
                repeat_count = 100
                #send_time = timeit.timeit(send_two_frames,number=repeat_count)
                send_time = timeit.timeit(
                    "send_two_hex_frames(client)",
                    setup="from __main__ import send_two_hex_frames, client",
                    number=repeat_count)
                # seconds per frame (spf) is send_time/number of frames so
                # fps is 1/spf = repeat_count * 2 / send_time
                fps = 2. * repeat_count / send_time
                print("sendframe rate: {:6.1f} fps (reps = {})".format(
                    fps, repeat_count))
            except KeyboardInterrupt:
                break
            
    elif args.mode == 'line':
        print("sending line")
        client.send_message("/line", [[0,0,10,10]])

    elif args.mode == 'clear':
        print("sending clear")
        client.send_message("/clear", True)
        
