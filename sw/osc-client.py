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

    # test for framerate: alternately light alternate pixels
    frame1 = "aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555"

    frame2 = "55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa"
    client.send_message("/hexframe", frame1)
    client.send_message("/hexframe", frame2)
 

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=5005,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    frame1 = "aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555"

    frame2 = "55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa"

    while True:
        repeat_count = 100                                                   
        #send_time = timeit.timeit(send_two_frames,number=repeat_count)     
        send_time = timeit.timeit("send_two_hex_frames(client)",
                                  setup="from __main__ import send_two_hex_frames, client",
                                  number=repeat_count)  
        # seconds per frame (spf) is send_time/number of frames so          
        # fps is 1/spf = repeat_count * 2 / send_time                       
        fps = 2.*repeat_count/send_time                                     
        print("sendframe rate: {:6.1f} fps (reps = {})".format(fps, repeat_count)) 
    
    # for x in range(10):
    #     client.send_message("/hexframe", frame1)
    #     client.send_message("/hexframe", frame2)
    #     time.sleep(0.1)
