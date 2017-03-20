#ifndef RACOM_TP_h
#define RACOM_TP_h

#include <Arduino.h>
#include "RACOM.h"
#include "RACOM_DL.h"

#define _TP_IDLE_STATE    	0
#define _TP_WAITING_STATE 	1
#define _TP_TIMEOUT_STATE	2
#define _TP_DATA_FULL_STATE	3

#define _ACK_CMD 0


class RACOM_TP {
  private:
    uint8_t* _data;
    uint8_t _cmd;
    uint16_t _dSize;
    int8_t _available;
	uint8_t _state = _TP_IDLE_STATE;
  public:
    RACOM_TP();
    uint8_t begin();
    void end();

    int8_t available();
    int8_t send(uint8_t cmd,uint16_t dSize,uint8_t* data);
    int8_t read(uint8_t* cmd,uint16_t* dSize,uint8_t* data);
	
    int8_t readSM();

    uint16_t dSize();
    uint8_t cmd();
};

extern RACOM_TP Racom;

#endif
