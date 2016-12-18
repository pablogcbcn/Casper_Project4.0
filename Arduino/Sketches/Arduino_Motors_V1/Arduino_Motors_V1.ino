#include <RacomI2C.h> // include RACOM lib

void setup() {
  Racom.begin(); // begin Transport layer
  pinMode(13,OUTPUT);
  digitalWrite(13,LOW);
}

void loop() {
  // first check if a packet is available
  if(Racom.available() == 1) {
    uint8_t cmd = Racom.cmd();
    uint16_t dSize = Racom.dSize(); 
    uint8_t *data = (uint8_t*)malloc(dSize);
    if(cmd==0x10){
      if(data[0] == 0)
        digitalWrite(13,LOW);
      else if(data[0] == 1)
        digitalWrite(13,HIGH);
    }
    
    //free the packet memory
    free(data);
    data = NULL;
  }
}
