import urllib3
import timeit
import sys

def send_two_frames():
    # to test timing, send two frames as rapidly as possible


    # 12.4fps with numerical hostname
    host = '192.168.1.145' 
    # 8.9fps with named host (bonjour?)
    #host = 'cm2.localhost' 

    url_str1 = "http://{}:8000/?frame=aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555".format(host)

    url_str2 = "http://{}:8000/?frame=55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa55555555aaaaaaaa".format(host)

    http = urllib3.PoolManager()
    try:
        r = http.request('GET', url_str1)
        r.close()
        r = http.request('GET', url_str2)
        r.close()

    except KeyboardInterrupt:
        # quit
        r.close()
        print("\nbye!")
        sys.exit()  

while(True):
    repeat_count = 10
    send_time = timeit.timeit(send_two_frames,number=repeat_count)      
    # seconds per frame (spf) is send_time/number of frames so          
    # fps is 1/spf = repeat_count * 2 / send_time                       
    fps = 2.*repeat_count/send_time                                     
    print("http frame rate: {:6.1f} fps (reps = {})".format(fps, repeat_count))


        
