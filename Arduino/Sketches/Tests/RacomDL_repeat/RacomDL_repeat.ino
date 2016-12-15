#include "RacomSensing.h" // needed to choose the used interface (see RacomSensing.h)
#include <RACOM.h> // include RACOM lib

void setup() {
  RacomDL.begin(); // begin Data Layer
}

void loop() {
  // first check if a packet is available
  if(RacomDL.available() == 1) {
    //read the size of the available packet
    uint8_t pSize = RacomDL.pSize(); 
    // allocate memory for the packet
    uint8_t *packet = malloc(pSize);
    // read the packet and test if the reading suceeded
    if(RacomDL.read(&pSize,packet)==1){
      //send back the exact same packet for testing purposes
      RacomDL.send(pSize,packet);
    }
    //free the packet memory
    free(packet);
    packet = NULL;
  }

}