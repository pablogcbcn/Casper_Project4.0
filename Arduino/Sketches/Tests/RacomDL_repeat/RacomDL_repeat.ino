#include <RacomI2C.h> // include RacomI2C or RacomSerial

void setup() {
  RacomDL.begin(); // begin Data Layer
  Serial.begin(115200);
}

void loop() {
  // first check if a packet is available
  if(RacomDL.available() == 1) {
    //read the size of the available packet
    uint8_t pSize = RacomDL.pSize(); 
    // allocate memory for the packet
    uint8_t *packet = (uint8_t*)malloc(pSize);
    // read the packet and test if the reading suceeded
    if(RacomDL.read(&pSize,packet)==1){
      //send back the exact same packet for testing purposes
      RacomDL.send(pSize,packet);
    }
    Serial.println("DONE");
    Serial.flush();
    //free the packet memory
    free(packet);
    packet = NULL;
  }
}
