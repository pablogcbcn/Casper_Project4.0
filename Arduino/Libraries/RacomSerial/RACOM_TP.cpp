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
	static uint32_t _t0;
	uint8_t okReply[] = {0,0,0,0};
	
	switch(this->_state) {
		case _TP_IDLE_STATE: {
			_t0 = millis();
			if(RacomDL.available()>0){
				this->_dSize = 0;
				uint8_t pSize = RacomDL.pSize();
				uint8_t tmp[pSize];
				RacomDL.read(&pSize,tmp);
				_data = (uint8_t*)malloc(pSize-2);
				this->_available=0;
				if(_data == NULL){
					okReply[1] = 0xFF;
					RacomDL.send(2,okReply);
					return -1;
				}
				switch(tmp[0]){
					case 0b00:{
						memcpy(this->_data+this->_dSize,tmp+2,pSize-2);
						this->_dSize += pSize-2;
						this->_state = _TP_DATA_FULL_STATE;
						okReply[1] = _ACK_CMD; // cmd = 0
						okReply[2] = this->_dSize&0xFF;
						okReply[3] = ((this->_dSize&0xFF00)>>8);
						RacomDL.send(4,okReply);
						return this->readSM();
					}break;
					case 0b01:{
						memcpy(this->_data+this->_dSize,tmp+2,pSize-2);
						this->_dSize += pSize-2;
						okReply[1] = _ACK_CMD; // cmd = 0
						okReply[2] = this->_dSize&0xFF;
						okReply[3] = ((this->_dSize&0xFF00)>>8);
						RacomDL.send(4,okReply);
						this->_state = _TP_WAITING_STATE;
						return 0;
					}break;
					default:
						return -1;
					break;
				}
			}
		}break;
		case _TP_WAITING_STATE: {
			if((millis()-_t0)>= TIMEOUT){
				okReply[1] = 0xFF; // error cmd
				RacomDL.send(2,okReply);
				free(this->_data);
				this->_data=NULL;
				this->_state=_TP_IDLE_STATE;
				this->_available = 0;
				return -1;
			}
			if(RacomDL.available()>0){
				uint8_t pSize = RacomDL.pSize();
				uint8_t tmp[pSize];
				RacomDL.read(&pSize,tmp);
				uint8_t* tmpPtr;
				tmpPtr = (uint8_t*)realloc(_data,_dSize+pSize-2);
				if(tmpPtr == NULL){
					okReply[1] = 0xFF; // error cmd
					RacomDL.send(2,okReply);
					free(this->_data);
					this->_data=NULL;
					this->_state=_TP_IDLE_STATE;
					this->_available = 0;
					return -1;
				}
				else
					_data=tmpPtr;
				switch(tmp[0]){
					case 0b11:{
						memcpy(_data+_dSize,tmp+2,pSize-2);
						this->_dSize+=pSize-2;
						okReply[1] = _ACK_CMD; // cmd = 0
						okReply[2] = this->_dSize&0xFF;
						okReply[3] = ((this->_dSize&0xFF00)>>8);
						RacomDL.send(4,okReply);
						this->_state=_TP_WAITING_STATE;
						return 0;
					}break;
					case 0b10:{
						memcpy(_data+_dSize,tmp+2,pSize-2);
						this->_dSize+=pSize-2;
						okReply[1] = _ACK_CMD; // cmd = 0
						okReply[2] = this->_dSize&0xFF;
						okReply[3] = ((this->_dSize&0xFF00)>>8);
						RacomDL.send(4,okReply);
						this->_state=_TP_DATA_FULL_STATE;
						return this->readSM();
					}break;
					default:
						okReply[1] = 0xFF; // error cmd
						RacomDL.send(2,okReply);
						free(this->_data);
						this->_data=NULL;
						this->_state=_TP_IDLE_STATE;
						this->_available = 0;
						return -1;
					break;
				}
			}
		}break;
		case _TP_DATA_FULL_STATE: {
			this->_available = 1;
			this->_state=_TP_IDLE_STATE;
			return 1;
		}break;
	}
	return 0;
}

RACOM_TP Racom = RACOM_TP();
