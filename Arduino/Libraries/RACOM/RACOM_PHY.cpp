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
    _TXcnt=0;
    _RXcnt=0;
    for(int i=0;i<sizeof(RacomPHY._TXBuffer);i++)
      RacomPHY._TXBuffer[i]=0;
  #endif
}

void RACOM_PHY::end(){
  #ifdef UART_INTERFACE
    Serial.end();
  #elif defined(I2C_INTERFACE)
    Wire.end();
  #endif
}

int8_t RACOM_PHY::available(){
  #ifdef UART_INTERFACE
    return Serial.available();
  #elif defined(I2C_INTERFACE)
    return _RXcnt;
  #endif
}

uint8_t RACOM_PHY::write(uint8_t val){
  #ifdef UART_INTERFACE
    return Serial.write(val);
  #elif defined(I2C_INTERFACE)
    _TXBuffer[_TXcnt]=val;
    _TXcnt+=1;
    return 1;
  #endif
}

uint8_t RACOM_PHY::write(uint8_t* buf,uint8_t len){
  #ifdef UART_INTERFACE
    return Serial.write(buf,len);
  #elif defined(I2C_INTERFACE)
    memcpy(_TXBuffer+_TXcnt,buf,len);
    _TXcnt+=len;
    return len;
  #endif
}

uint8_t RACOM_PHY::read(){
  #ifdef UART_INTERFACE
    return Serial.read();
  #elif defined(I2C_INTERFACE)
    uint8_t b = RacomPHY._RXBuffer[0];
    memcpy(_RXBuffer,_RXBuffer+1,_RXcnt);
    _RXcnt -= 1;
    return b;
  #endif
}

#ifdef I2C_INTERFACE
static void RACOM_PHY::receiveEvent(int n) {
  // check if byte received when reading by the rpi
  RacomPHY._LBsize = Wire.available();
  Serial.print("Received: ");
  while (Wire.available()>0){
    RacomPHY._RXBuffer[RacomPHY._RXcnt]=Wire.read();
    RacomPHY._RXcnt++;
    Serial.print(RacomPHY._RXBuffer[RacomPHY._RXcnt-1]);
    Serial.print(" ");
  }
  Serial.println("");
  
}

static void RACOM_PHY::requestEvent() {
  Serial.print("TX buffer: ");
  for(uint8_t i=0;i<RacomPHY._TXcnt;i++) {
    Serial.print(RacomPHY._TXBuffer[i]);
    Serial.print(" ");
  }
  Serial.println("");
  RacomPHY._RXcnt -= 1;
  uint8_t toRead = RacomPHY._RXBuffer[RacomPHY._RXcnt];
  if(toRead>RacomPHY._TXcnt)
    return;
  Wire.write(RacomPHY._TXBuffer,toRead);
  memcpy(RacomPHY._TXBuffer,RacomPHY._TXBuffer+toRead,sizeof(RacomPHY._TXBuffer)-toRead);
  RacomPHY._TXcnt -= toRead;
  
}
#endif

RACOM_PHY RacomPHY = RACOM_PHY();
