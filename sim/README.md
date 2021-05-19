


# Simple py3 server to simulate LED panel display.

Usage: send a GET request to the http:/ip:port url this server is running on,
followed by "'data?'"  then a 256-char hex string. Each hex digit
represents 4 LED bits in row-major order, each of 32 rows row is
represented by 8 hex digits.  e.g to will draw a box around the display

> curl -s http://127.0.0.1:8000/data?FFFFFFFF800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001FFFFFFFF

other methods:

'/display': turn display on or off, zero for off, nonzero int to turn on
> curl -s http://127.0.0.1:8000/display?0

'/bright': set brightness, integer 0-15
>curl -s http://127.0.0.1:8000/bright:15

adapted from https://gist.github.com/kylemcdonald/3bb71e4b901c54073cbc
