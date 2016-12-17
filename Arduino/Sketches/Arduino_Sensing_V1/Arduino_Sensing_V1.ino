#include <RacomSerial.h>
#include"Arduino_sensing_V1.h"

void setup() {
  Wire.begin();
  Racom.begin();
}

void loop() {
  
  if(Racom.available() == 1) {
    // read the cmd byte
    uint8_t cmd = Racom.cmd();
    //read the size of the available data
    uint16_t dSize = Racom.dSize(); 
    // allocate memory for the data
    uint8_t *data = (uint8_t*)malloc(dSize);
    Racom.read(&cmd,&dSize,data);
    
    if(cmd >= 0x10){
      if(cmd%2 == 0){
        switch(cmd){
          case get_I2C_Register:
            I2C_Init(dSize, data, _address, _register, _value);
            I2C_Receive(_address, _register, _value);
            Racom.send(get_I2C_Register, 1, _value);
            I2C_End(_address, _register, _value);
            break;
          case get_SPI_Register:
            break;
          case get_GPIO:
            break;
        }
      }else{
        switch(cmd){
          case set_I2C_Register:
            I2C_Init(dSize, data, _address, _register, _value);
            I2C_Send(_address, _register, _value);
            I2C_End(_address, _register, _value);
            break;
          case set_SPI_Register:
            break;
          case set_GPIO:
            break;
          case set_PinMode:
            break;
        }
      }
    }
    free(data);
    data = NULL;
  }
}

void I2C_Init(uint16_t dSize, uint8_t* data, uint8_t* _address, uint8_t* _register, uint8_t* _value){
  
  _address = (uint8_t*)malloc(1);
  _register = (uint8_t*)malloc(1);
  _value = (uint8_t*)malloc(1);
  for(int i = 0; i < 3; i++){
    switch(i){
      case 0:
        *_address = *(data + i);
        break;
      case 1:
        *_register = *(data + i);
        break;
      case 2:
        if(i < dSize){
          *_value = *(data + i);
        }
        break;
    }
  }
}

void I2C_Send(uint8_t* _address, uint8_t* _register, uint8_t* _value){
  Wire.beginTransmission(*_address);
  Wire.write(*_register);
  Wire.write(*_value);
  Wire.endTransmission();
}

void I2C_Receive(uint8_t* _address, uint8_t* _register, uint8_t* _value){
  Wire.beginTransmission(*_address);    // Get the slave's attention, tell it we're sending a command byte
  Wire.write(*_register);                               //  The command byte, sets pointer to register with address of _register
  Wire.requestFrom(*_address,1);          // Tell slave we need to read 1byte from the current register
  *_value = Wire.read();        // read that byte into _value variable
  Wire.endTransmission();                  // "Hang up the line" so others can use it (can have multiple slaves & masters connected)
}

void I2C_End(uint8_t* _address, uint8_t* _register, uint8_t* _value){

  free(_address);
  free(_register);
  free(_value);
}

