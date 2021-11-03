## CM2 panel Python software


Low-level driver code for the RPI is in `htlib` directory. See the README there. That code is compiled for the library `libht1632c-py.so` which must be in this directory or in the python load path. 

Several test programs exist to excercise the CM2 display panel. 'setxy.py' turns on a pixel at x and y, for example to turn on a pixel at x=10 and y=11 type:

```console
$ python setxy.py 10 11
```

The `testpattern.py`

## The CM2 HTTP Server

`cm2_server.py` drives the display by running an http server at port
8000 and responding to query strings in the URL of a GET request. To
send a frame of data, send 128 characters of hexadecimal data in
column-major order with the `frame` query parameter. Each 8 hex
characters represent 32 bits in one column of LEDs. For example the
following curl command will send data to light the leftmost and rightmost
columns and top and bottom rows, drawing a box around the perimeter of
the display.


```console
$ curl -s 'http://cm2.local:8000/?frame=FFFFFFFF800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001800000018000000180000001FFFFFFFF'
```

Other query parameters are:

* `?bright=n` sets the PWM brightness where `n` is an integer between 0
  and 15.

* `?x=10&y=10&text=HELLO%20WORLD` will display the text "HELLO WORLD"
  with URL encoding at position x, y. If the `x` and `y` parameters
  are not specified the default position of zero (top left corner) is
  used. Negative positions can be used so that decrementing the x
  position will scroll the text left to right so that text wider than
  32 pixels can be displayed sequentially. 

As usual, multiple parameters may be used in one command, for example the following command will display text at 10, 10 with a brightness of 25%

```console
$ curl -s 'http://cm2.local:8000/?x=10&y=10&bright=4&&text=Hello%20World'
```
