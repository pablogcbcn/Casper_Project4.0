#include "RACOM_DL.h"

RACOM_DL::RACOM_DL() { 
}

void RACOM_DL::begin() {
  this->_available = 0;
  this->_pSize = 0;
  this->_cnt = 0;
  this->_packet = (uint8_t*) malloc(MAX_PDATA_SIZE+2);
  RacomPHY.begin();
}

void RACOM_DL::end() {
  free(this->_packet);
  this->_packet = NULL;
  RacomPHY.end();
}

uint8_t RACOM_DL::send(uint8_t pSize, uint8_t* packet) {
	//RacomPHY.flushTx();
	RacomPHY.write(_STX);
	RacomPHY.write((uint8_t)(pSize<<2) + (packet[0] & 0b11));
	if(pSize==2)
		RacomPHY.write(*(packet+1));
	else if(pSize>2)
		RacomPHY.write((packet+1),(pSize-1));
	return 1;
}

uint8_t RACOM_DL::pSize(){
  if(_available==1)
    return _pSize;
  else
    return 0;
}

int8_t RACOM_DL::read(uint8_t* pSize, uint8_t* packet) {
  if(this->available()==1){
    *pSize = this->_pSize;
	memcpy(packet,this->_packet,this->_pSize);
    this->_available = 0;
    return 1;
  }
  else
    return 0;
}

void RACOM_DL::flushRx() {
  RacomPHY.flushRx();
  this->_state = _WAITING_STATE;
  this->_available = 0;
}

void RACOM_DL::flushTx() {
  RacomPHY.flushTx();
  //this->_state = _WAITING_STATE;
  this->_available = 0;
}

int8_t RACOM_DL::available(){
	int8_t code = this->readSM();
	if(code<0){
		//RacomDL.end();
		//RacomDL.begin();
		return code;
	}
	return this->_available;
}

int8_t RACOM_DL::readSM() {
  static uint32_t _t0;
  
  switch(this->_state) {
    case _WAITING_STATE: {
		_t0 = millis();
		uint8_t tmp = 0;
		while(RacomPHY.available()!=0 && tmp !=_STX){
			tmp = RacomPHY.read();
		}
		if(tmp==_STX){
			this->_state = _START_STATE;
			this->_cnt = 0;
			_t0 = millis();
			this->_available = 0;
		}
		}
		break;
      
    case _START_STATE:{
		if(RacomPHY.available()>0 && this->_available <= 0) {
			uint8_t tmp = RacomPHY.read();
			this->_pSize = tmp >> 2;
			this->_packet[0] = tmp & 0b11;
			this->_cnt+=1;
			this->_state = _WAIT_DATA_STATE;
		}
		else if((millis()-_t0)>= TIMEOUT){
			this->_state = _WAITING_STATE;
			this->_available = 0;
			return -1;
		}
		}
		break;
      
    case _WAIT_DATA_STATE:{
		while(RacomPHY.available()>0&&_cnt<=(_pSize-1)) {
			this->_packet[_cnt] = RacomPHY.read();
			this->_cnt+=1;
		}
		if(_cnt==(_pSize)){
			this->_available = 1;
			this->_state = _WAITING_STATE;
			//RacomPHY.flushRx();
			return 1;
		}
		else if((millis()-_t0)>= TIMEOUT){
			this->_state = _WAITING_STATE;
			this->_available = 0;
			return -2;
		}
		}
		break;      
  }
  return 0;
}

#ifdef UART_INTERFACE
void serialEvent(){
  if(RacomPHY.available()>0){
      //RacomDL.readSM();
  }
}
#elif defined(I2C_INTERFACE)

#endif

RACOM_DL RacomDL = RACOM_DL();

