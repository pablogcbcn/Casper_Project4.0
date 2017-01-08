#include <RacomSerial.h> // include RACOM lib
#include <DynamixelR.h>
#include"Arduino_Motors_V2.h"

void setup() {
  Racom.begin(); // begin Transport layer
  delay(100);
  dynamixel.Begin(0,115200,&Serial);
}

void loop() {
  // first check if a packet is available

  if(Racom.available() == 1) {
    uint8_t cmd = Racom.cmd();
    uint16_t dSize = Racom.dSize(); 
    uint8_t* data = (uint8_t*)malloc(dSize);
    Racom.read(&cmd,&dSize,data);
    switch(cmd){
      case dynamixel_Move:
        dynamixel.Goal_position(data[0],data[1]);
        break;
    }
    
    //free the packet memory
    free(data);
    data = NULL;
  }
}
