#include <RacomSerial.h> // include RACOM lib

void setup() {
  Racom.begin(); // begin Transport layer

}

void loop() {
  // first check if a packet is available
  if(Racom.available() == 1) {
    // read the cmd byte
    uint8_t cmd = Racom.cmd();
    //read the size of the available data
    uint16_t dSize = Racom.dSize(); 
    // allocate memory for the data
    uint8_t *data = (uint8_t*)malloc(dSize);
    // read the data and test if the reading suceeded
    if(Racom.read(&cmd,&dSize,data)==1){
//      for(uint8_t i =0;i<dSize;i++){
//        Serial.print(data[i]);
//        Serial.print(" ");
//      }
//      Serial.println("");
      //send back the exact same packet for testing purposes
      Racom.send(cmd,dSize,data);
    }
    //free the packet memory
    free(data);
    data = NULL;
  }
}
