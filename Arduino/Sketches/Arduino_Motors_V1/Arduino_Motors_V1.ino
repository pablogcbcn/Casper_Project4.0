#include <RacomSerial.h> // include RACOM lib
#include <DynamixelSoftSerial.h>

#define MOTOR_ID 9

void setup() {
  Racom.begin(); // begin Transport layer
  delay(100);
  Dynamixel.begin(9600,2);
  delay(100);
  pinMode(13,OUTPUT);
  digitalWrite(13,LOW);
}

void loop() {
  // first check if a packet is available

  if(Racom.available() == 1) {
    uint8_t cmd = Racom.cmd();
    uint16_t dSize = Racom.dSize(); 
    uint8_t* data = (uint8_t*)malloc(dSize);
    Racom.read(&cmd,&dSize,data);
    if(cmd==0x10){
      if(data[0] == 0){
        digitalWrite(13,HIGH);
        Dynamixel.move(MOTOR_ID,100);
      }
      else if(data[0] == 1){
        digitalWrite(13,LOW);
        Dynamixel.move(MOTOR_ID,900);
      }
    }
    
    //free the packet memory
    free(data);
    data = NULL;
  }
}
