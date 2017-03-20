#ifndef RACOM_PHY_H
#define RACOM_PHY_H

#include <Arduino.h>
#include "RACOM.h"
#include "Wire.h"

class RACOM_PHY {
    #ifdef I2C_INTERFACE
    
    #endif
  public:
    #ifdef I2C_INTERFACE
	uint8_t _TXBuffer[32];
    uint8_t _RXBuffer[32];
    uint8_t _TXcnt;
    uint8_t _RXcnt;
    #endif
    
    RACOM_PHY();

    void begin();
    void end();

    int8_t available();
    uint8_t write(uint8_t val);
    uint8_t write(uint8_t* buf,uint8_t len);
    uint8_t read();
	
	void flushRx();
	void flushTx();
    //static void requestEvent();
};
void receiveEvent(int n);
void requestEvent();

extern RACOM_PHY RacomPHY;

#endif
