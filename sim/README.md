


# Simple py3 server to simulate LED panel display.

Usage: `python py3_32x32_sim.py`


When server is running, send a `GET` request to the `http://ip:port`
url, followed by "`/data?`" then a 256-char hex string. Each hex digit
represents 4 LED bits in row-major order, each of the subsequent 32 rows is
represented by successive 8 hex digits.  

Example: to  draw a box around the
outer LEDs of the 32x32 display:

> curl -s http://127.0.0.1:8000/data?FFFFFFFF800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001FFFFFFFF

other methods:

`/display?`: turn display on or off, zero for off, nonzero int to turn on
> curl -s http://127.0.0.1:8000/display?0

`/bright?`: set brightness, integer 0-15
>curl -s http://127.0.0.1:8000/bright:15

`curltest.sh`is a bash script to test the server by repeatedly sending two different frames. 

server based on https://gist.github.com/kylemcdonald/3bb71e4b901c54073cbc


Example output of the simulator:
```query is FFFFFFFF800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001FFFFFFFF
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - * 
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
```
