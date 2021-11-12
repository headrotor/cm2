#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

// #include "wiringPi.h"

#include "ht1632c.h"
#include "rotenc.h"

#define NUM_PANELS 1
#define PANEL_ROTATION 0
#define WIDTH (NUM_PANELS * 32)
#define HEIGHT 32

#define ROTENC_PIN_0 3
#define ROTENC_PIN_1 4
#define ROTENC_PIN_BTN 2


int main(int argc, char *argv[]) {
	
  printf("test: init ht1632c\n");
  ht1632c_init(NUM_PANELS, PANEL_ROTATION);
  if(argc == 2){
    
    int count = ht1632c_hexframe(argv[1]);
    ht1632c_sendframe();
    printf("sent %d chars\n", count);
  }
  ht1632c_close();
}
