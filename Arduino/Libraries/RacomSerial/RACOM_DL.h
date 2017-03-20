#ifndef RACOM_DL_h
#define RACOM_DL_h

#include <Arduino.h>
#include "RACOM.h"
#include "RACOM_PHY.h"

#define _WAITING_STATE 0
#define _START_STATE 1
#define _WAIT_DATA_STATE 2

#define _STX   0x02

class RACOM_DL {
  private:
    uint8_t* _packet;
    uint8_t _pSize;
    uint8_t _cnt;
    int8_t _available;
	uint8_t _state = _WAITING_STATE;
  public:
    RACOM_DL();
    void begin();
    void end();
    
    int8_t available();
    
    uint8_t send(uint8_t pSize, uint8_t* packet);
    int8_t read(uint8_t* pSize, uint8_t* packet);
    int8_t readSM();
    void  flushRx();
	void  flushTx();

    uint8_t pSize();
    
};

extern RACOM_DL RacomDL;

void receiveEvent(int n);

#endif

