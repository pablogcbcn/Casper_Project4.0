#include "RacomSensing.h"
#include <RACOM.h>

void setup() {
  RacomDL.begin();

//  uint8_t packet[] = {0,1,2,3,4,5,6,7};
//  RacomDL.send(sizeof(packet),packet);
//  
}

void loop() {
  if(RacomDL.available() == 1) {
    uint8_t pSize = RacomDL.pSize(); 
    uint8_t *packet = malloc(pSize);
    if(RacomDL.read(&pSize,packet)==1){
      RacomDL.send(pSize,packet);
    }
    free(packet);
    packet = NULL;
  }

}
