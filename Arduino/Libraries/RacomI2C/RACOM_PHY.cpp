#include "RACOM_PHY.h"
RACOM_PHY::RACOM_PHY(){
}
  
void RACOM_PHY::begin(){
  #ifdef UART_INTERFACE
    Serial.begin(UART_BAUDRATE);
  #elif defined(I2C_INTERFACE)
    Wire.begin(I2C_ADDRESS);
    Wire.onRequest(requestEvent);
    Wire.onReceive(receiveEvent);
    RacomPHY._TXcnt=0;
    RacomPHY._RXcnt=0;
    for(uint8_t i=0;i<sizeof(RacomPHY._TXBuffer);i++){
	  RacomPHY._RXBuffer[i]=0;
	  RacomPHY._TXBuffer[i]=0;
	}
	delay(50);
  #endif
}

void RACOM_PHY::end(){
  #ifdef UART_INTERFACE
    Serial.end();
  #elif defined(I2C_INTERFACE)
	RacomPHY.flushRx();
	RacomPHY.flushTx();
    Wire.end();
  #endif
}

void RACOM_PHY::flushRx(){
  while(RacomPHY.available()!=0)
	  RacomPHY.read();
}
void RACOM_PHY::flushTx(){
  #ifdef I2C_INTERFACE
	RacomPHY._TXcnt = 0;
  #endif
}
int8_t RACOM_PHY::available(){
  #ifdef UART_INTERFACE
    return Serial.available();
  #elif defined(I2C_INTERFACE)
    return RacomPHY._RXcnt;
  #endif
}

uint8_t RACOM_PHY::write(uint8_t val){
  #ifdef UART_INTERFACE
    return Serial.write(val);
  #elif defined(I2C_INTERFACE)
    RacomPHY._TXBuffer[_TXcnt]=val;
    RacomPHY._TXcnt+=1;
    return 1;
  #endif
}

uint8_t RACOM_PHY::write(uint8_t* buf,uint8_t len){
  #ifdef UART_INTERFACE
    return Serial.write(buf,len);
  #elif defined(I2C_INTERFACE)
    memcpy(_TXBuffer+_TXcnt,buf,len);
    RacomPHY._TXcnt+=len;
	while(RacomPHY._TXcnt!=0){
		delay(1);
	}
    return len;
  #endif
}

uint8_t RACOM_PHY::read(){
  #ifdef UART_INTERFACE
    return Serial.read();
  #elif defined(I2C_INTERFACE)
    uint8_t b = RacomPHY._RXBuffer[0];
    memcpy(_RXBuffer,_RXBuffer+1,_RXcnt);
    RacomPHY._RXcnt -= 1;
    return b;
  #endif
}

#ifdef I2C_INTERFACE
void receiveEvent(int n) {
  while(Wire.available()>0){
	RacomPHY._RXBuffer[RacomPHY._RXcnt]=Wire.read();
	RacomPHY._RXcnt+=1;
  }
  
}

void requestEvent() {
  RacomPHY._RXcnt -= 1;
  uint8_t toRead = RacomPHY._RXBuffer[RacomPHY._RXcnt];
  if(toRead>RacomPHY._TXcnt || toRead ==0){
	for(uint8_t i;i<toRead;i++)
		Wire.write(0);
	RacomPHY.end();
	RacomPHY.begin();
    return;
  }

  Wire.write(RacomPHY._TXBuffer,toRead);
  memcpy(RacomPHY._TXBuffer,RacomPHY._TXBuffer+toRead,sizeof(RacomPHY._TXBuffer)-toRead);
  RacomPHY._TXcnt -= toRead;
}
#endif

RACOM_PHY RacomPHY = RACOM_PHY();

