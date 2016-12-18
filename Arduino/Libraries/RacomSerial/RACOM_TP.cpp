#include "RACOM_TP.h"

RACOM_TP::RACOM_TP () {
}

uint8_t RACOM_TP::begin() {
  RacomDL.begin();
  Serial.println("init");
  this->_available = 0;
  return 1;
}

void RACOM_TP::end(){
  RacomDL.end();
  free(_data);
  _data = NULL;
}

uint16_t RACOM_TP::dSize(){
  if(_available==1){
    return _dSize;
  }
  else
    return 0;
}

uint8_t RACOM_TP::cmd(){
  if(_available==1){
    return _cmd;
  }
  else
    return 0;
}

int8_t RACOM_TP::send(uint8_t cmd,uint16_t dSize,uint8_t* data){
  uint16_t nPacket;
  if(dSize % MAX_PDATA_SIZE ==0)
    nPacket = dSize/MAX_PDATA_SIZE;
  else
    nPacket = floor(dSize/MAX_PDATA_SIZE)+1;
  uint8_t packet[MAX_PDATA_SIZE+2];
  
  if(nPacket == 1)
    packet[0]=0b00;
  else
    packet[0]=0b01;
  
  packet[1] = cmd;

  for(uint16_t i =0; i<nPacket;i++) {
    uint16_t j=0;
    for(j=0;j<MAX_PDATA_SIZE&&i*MAX_PDATA_SIZE+j<dSize;j++){
      packet[2+j] = data[i*MAX_PDATA_SIZE+j];
    }
    RacomDL.flushRx();
    RacomDL.send(j+2,packet);
    int8_t code = RacomDL.available();
    while(code != 1){
      if(code<0)
        return code;
      code = RacomDL.available();
    }
    uint8_t replySize = RacomDL.pSize();
    uint8_t reply[replySize];
    RacomDL.read(&replySize,reply);
    uint16_t checkSize = reply[2] +((uint16_t)reply[3]<<8);
    if(checkSize!=i*MAX_PDATA_SIZE+j)
      return -1;
    packet[0]=0b11;
    if(i==nPacket-2)
      packet[0]=0b10;
  }
  return nPacket;
}

int8_t RACOM_TP::available(){
  //return this->readSM();
  int8_t code = this->readSM();
  if(code<0){
    free(_data);
    _data = NULL;
    _dSize = 0;
    return code;
  }
  return this->_available;
}

int8_t RACOM_TP::read(uint8_t* cmd,uint16_t* dSize,uint8_t* data){
  if(_available==1) {
    *dSize = _dSize;
    *cmd = _cmd;
    memcpy(data,_data,_dSize);
    _available = 0;
    free(_data);
    _data = NULL;
    _dSize=0;
    return 1;
  }
  return _available;
}

int8_t RACOM_TP::readSM(){
  uint8_t okReply[] = {0,0,0,0};
  int8_t dlStatus = RacomDL.available();
  if(dlStatus < 0) {
    // Timeout of receiving packet
    _available = -1;
    RacomDL.flushRx();
    return -1;
  }
  else if(dlStatus >0) {
    uint8_t pSize = RacomDL.pSize();
    
    uint8_t tmp[pSize];
    RacomDL.read(&pSize,tmp);
    uint8_t pFlags = tmp[0];
    RacomDL.flushRx();
    
    if(_data == NULL) {
      _data = (uint8_t*)malloc(pSize-2);
      if(_data == NULL){
        okReply[1] = 0xFF;
        RacomDL.send(2,okReply);
      }
      _available=0;
    }
    else {
      
      uint8_t* tmpPtr;
      tmpPtr = (uint8_t*)realloc(_data,_dSize+pSize-2);
      if(tmpPtr != NULL)
        _data=tmpPtr;
      else {
        _available = -1;
        okReply[1] = 0xFF; // error cmd
        RacomDL.send(4,okReply);
        free(_data);
        _data=NULL;
        _dSize = 0;
        return -1;
      }
    }
    _cmd = tmp[1];
    // set data of the reply to _dSize+pSize-2
    okReply[1] = 0; // cmd = 0
    uint16_t s = _dSize+pSize-2;
    okReply[2] = s&0xFF;
    okReply[3] = ((s&0xFF00)>>8);
    
    switch(pFlags) {
      case 0b00: {
        _dSize = 0;
        memcpy(_data+_dSize,tmp+2,pSize-2);
        _dSize+=pSize-2;
        RacomDL.send(4,okReply);
        _available = 1;
        return 1;
      } break;
      case 0b01: {
        _dSize = 0;
        memcpy(_data+_dSize,tmp+2,pSize-2);
        _dSize+=pSize-2;
        RacomDL.send(4,okReply);
        _available = 0;
        return 0;
      } break;
      case 0b11: {
        memcpy(_data+_dSize,tmp+2,pSize-2);
        _dSize+=pSize-2;
        RacomDL.send(4,okReply);
        _available = 0;
        return 0;
      } break;
      case 0b10: {
        memcpy(_data+_dSize,tmp+2,pSize-2);
        _dSize+=pSize-2;
        RacomDL.send(4,okReply);
        _available = 1;
        return 1;
      } break;
      default : {
        okReply[1] = 0xFF;
        RacomDL.send(4,okReply);
        _available = -1;
        return -1;
      } break;
    }
    RacomDL.send(4,okReply);
    return _available;
  }
  else
    return 0;
}

RACOM_TP Racom = RACOM_TP();
