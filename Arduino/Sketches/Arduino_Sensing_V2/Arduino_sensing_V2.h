#ifndef ARDUINO_SENSING_V2_H
#define ARDUINO_SENSING_V2_H

#define get_I2C_Register  0x10
#define set_I2C_Register  0x11
#define get_I2C_Word      0x12
#define set_I2C_Word      0x13
#define get_SPI_Register  0x14
#define set_SPI_Register  0x15
#define get_GPIO          0x16
#define set_GPIO          0x17
#define set_PinMode       0x19

uint8_t* _address;
uint8_t* _register;
uint8_t* _value;

#endif
