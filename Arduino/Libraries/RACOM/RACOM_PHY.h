#ifndef RACOM_PHY_H
#define RACOM_PHY_H

#include "RACOM.h"
#include "Wire.h"

class RACOM_PHY {
  private:
    #ifdef I2C_INTERFACE
    uint8_t _TXBuffer[32];
    uint8_t _RXBuffer[32];
    uint8_t _TXcnt;
    uint8_t _RXcnt;
    static void receiveEvent(int n);
    static void requestEvent();
    #endif
  public:
    #ifdef I2C_INTERFACE
    uint8_t _LBsize;
    #endif
    
    RACOM_PHY();

    void begin();    
    void end();

    int8_t available();
    uint8_t write(uint8_t val);
    uint8_t write(uint8_t* buf,uint8_t len);
    uint8_t read();

    //static void requestEvent();
    
};

extern RACOM_PHY RacomPHY;

#endif
