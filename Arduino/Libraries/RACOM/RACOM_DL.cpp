#include "RACOM_DL.h"

RACOM_DL::RACOM_DL() { 
}

void RACOM_DL::begin() {
  _available = 0;
  _pSize = 0;
  _cnt = 0;
  _packet = malloc(MAX_FDATA_SIZE+2);
  RacomPHY.begin();
  
}

void RACOM_DL::end() {
  free(_packet);
  _packet = NULL;
  RacomPHY.end();
}

uint8_t RACOM_DL::send(uint8_t pSize, uint8_t* packet) {
  RacomPHY.write(_STX);
  RacomPHY.write((uint8_t)(pSize<<2) + (packet[0] & 0b11));
  if(pSize==2)
    RacomPHY.write(*(packet+1));
  else if(pSize>2)
    RacomPHY.write((packet+1),(pSize-1));
}

int8_t RACOM_DL::available(){
  this->readSM();
  return _available;
}

uint8_t RACOM_DL::pSize(){
  if(_available==1)
    return _pSize;
  else
    return 0;
}

int8_t RACOM_DL::read(uint8_t* pSize, uint8_t* packet) {
  if(_available==1){
    *pSize = _pSize;
    for(uint8_t i = 0;i<_pSize;i++){
      packet[i]=_packet[i];
    }
    _available = 0;
    return 1;
  }
  else
    return _available;
}

void RACOM_DL::flushRx() {
  while(RacomPHY.available()!=0)
    RacomPHY.read();
  this->_available = 0;
}

int8_t RACOM_DL::readSM() {
  static uint8_t _state = _WAITING_STATE;
  static uint32_t _t0;
  
  switch(_state) {
    case _WAITING_STATE: {
      uint8_t tmp = 0;
      while(RacomPHY.available()!=0){
        tmp = RacomPHY.read();
        if(tmp==_STX) {
          _cnt = 0;
          break;
        }
      }
      if(tmp==_STX)
        _state = _START_STATE;
    }
    break;
      
    case _START_STATE:
      _t0 = millis();
      if(RacomPHY.available()>0 && _available <= 0) {
        uint8_t tmp = RacomPHY.read();
        _pSize = tmp >> 2;
        _packet[0] = tmp & 0b11;
        _cnt = 1;
      }
      if(_cnt == 1) {
        _state = _WAIT_DATA_STATE;
      }
      else if((millis()-_t0)>= TIMEOUT){
        _state = _WAITING_STATE;
        _available = -1;
        return -1;
      }
      break;
      
    case _WAIT_DATA_STATE:
      while(RacomPHY.available()>0&&_cnt<_pSize) {
        _packet[_cnt] = RacomPHY.read();
        _cnt+=1;
      }
      if((millis()-_t0)>= TIMEOUT){
        _state = _WAITING_STATE;
        _available = -1;
        return -1;
      }
      else if(_cnt==(_pSize)){
        _available = 1;
        _state = _WAITING_STATE;
        return 1;
      }
      break;      
  }
  return 0;
}

#ifdef UART_INTERFACE
void serialEvent(){
  if(RacomPHY.available()>0){
    #ifdef DL_EN
      RacomDL.readSM();
    #endif
  }
}
#elif defined(I2C_INTERFACE)

#endif

RACOM_DL RacomDL = RACOM_DL();

