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
    uint8_t* reply;
    if(cmd >= 0x10){
      if(cmd%2 == 0){
        switch(cmd){
          case get_I2C_Register:
            reply = (uint8_t*)malloc(1);
            I2C_Init(dSize, data, _address, _register, _value);
            I2C_Receive(&data[0], &data[1], &reply[0]);
            Racom.send(get_I2C_Register, 1, &reply[0]);
            I2C_End(_address, _register, _value);
            free(reply);
            reply = NULL;
            break;
          case get_I2C_Word:
            reply = (uint8_t*)malloc(2);
            I2C_Init(dSize, data, _address, _register, _value);
            I2C_Receive_Word(&data[0], &data[1], reply);
            Racom.send(get_I2C_Register, 2, reply);
            I2C_End(_address, _register, _value);
            free(reply);
            reply = NULL;
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
            I2C_Send(&data[0], &data[1], &data[2]);
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

  _address[0] = data[0];
  _register[0] = data[1];
  _value[0] = data[2];
}

void I2C_Send(uint8_t* _address, uint8_t* _register, uint8_t* _value){
  Wire.beginTransmission(_address[0]);
  Wire.write(_register[0]);
  Wire.write(_value[0]);
  Wire.endTransmission();
}

void I2C_Receive(uint8_t* address, uint8_t* reg, uint8_t* value){
  Wire.beginTransmission(address[0]);    // Get the slave's attention, tell it we're sending a command byte
  Wire.write(reg[0]);                               //  The command byte, sets pointer to register with address of _register
  Wire.endTransmission();
  while (Wire.requestFrom(address[0],1) != 1);          // Tell slave we need to read 1byte from the current register
  value[0] = Wire.read();        // read that byte into _value variable
}

void I2C_Receive_Word(uint8_t* address, uint8_t* reg, uint8_t* value){
  Wire.beginTransmission(address[0]);    // Get the slave's attention, tell it we're sending a command byte
  Wire.write(reg[0]);                               //  The command byte, sets pointer to register with address of _register
  Wire.endTransmission();
  while (Wire.requestFrom(address[0],2) != 2);          // Tell slave we need to read 1byte from the current register
  value[0] = Wire.read();        // read that byte into _value variable
  value[1] = Wire.read();
}


void I2C_End(uint8_t* _address, uint8_t* _register, uint8_t* _value){

  free(_address);
  free(_register);
  free(_value);
}

