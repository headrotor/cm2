import requests
import timeit
import sys

def send_two_frames():
    # to test timing, send two frames as rapidly as possible


    # faster with numerical host?
    host = '192.168.1.145' 
    #host = 'cm2.localhost' 

    url_str1 = "http://{}:8000/?frame=aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555".format(host)

    url_str2 = "http://{}:8000/?frame=55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa".format(host)

    s = requests.Session()
    # does keepalive by default -- doesn't seem to help???
    try:
        r = s.get(url_str1)
        r = s.get(url_str2)
        #r.close()
        #r = http.request('GET', url_str2)
        #r.close()

    except KeyboardInterrupt:
        # quit
        print("\nbye!")
        sys.exit()  

while(True):
    repeat_count = 10
    send_time = timeit.timeit(send_two_frames,number=repeat_count)      
    # seconds per frame (spf) is send_time/number of frames so          
    # fps is 1/spf = repeat_count * 2 / send_time                       
    fps = 2.*repeat_count/send_time                                     
    print("http frame rate: {:6.1f} fps (reps = {})".format(fps, repeat_count))


        
