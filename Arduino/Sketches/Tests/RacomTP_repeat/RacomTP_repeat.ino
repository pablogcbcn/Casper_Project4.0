#include "RacomSensing.h" // needed to choose the used interface (see RacomSensing.h)
#include <RACOM.h> // include RACOM lib

void setup() {
  Racom.begin(); // begin Transport layer
}

void loop() {
  // first check if a packet is available
  if(Racom.available() == 1) {
    //read the size of the available data
    uint16_t dSize = Racom.dSize(); 
    // allocate memory for the packet
    uint8_t *data = malloc(dSize);
    // read the packet and test if the reading suceeded
    if(Racom.read(&dSize,data)==1){
      //send back the exact same packet for testing purposes
      Racom.send(dSize,data);
    }
    //free the packet memory
    free(data);
    data = NULL;
  }

}
