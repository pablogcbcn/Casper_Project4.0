#ifndef RACOM_h
#define RACOM_h

#include <Arduino.h>

#define PHY_EN
#define DL_EN
#define TP_EN

#if !defined(UART_INTERFACE) && !defined(I2C_INTERFACE)
#define UART_INTERFACE  // default interface
#endif

// Serial interface options
#ifdef  UART_INTERFACE
#define UART_BAUDRATE 115200

// I2C interface options
#elif  defined(I2C_INTERFACE)
#define I2C_ADDRESS 8

#endif

// Communication settings
#define TIMEOUT 100
#ifdef UART_INTERFACE
#define RACOM_RX_BUFFER SERIAL_RX_BUFFER_SIZE
#elif defined(I2C_INTERFACE)
#define RACOM_RX_BUFFER 32
#endif
#define MAX_FDATA_SIZE (RACOM_RX_BUFFER-4)


#include "RACOM_TP.h"

#endif
