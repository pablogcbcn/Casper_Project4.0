#ifndef RACOM_h
#define RACOM_h

//-----PHY Options---------

#define UART_INTERFACE  // default interface, to change to select between I2C and Serial

#ifdef  UART_INTERFACE
	#define UART_BAUDRATE 115200
#elif  defined(I2C_INTERFACE)
	#define I2C_ADDRESS 8
#endif

//-----DL Options----------

#ifdef UART_INTERFACE
	#ifdef ESP_H // if an ESP8266 based arduino is used
		#define RACOM_RX_BUFFER 64
	#else
		#define RACOM_RX_BUFFER SERIAL_RX_BUFFER_SIZE
	#endif
#elif defined(I2C_INTERFACE)
	#define RACOM_RX_BUFFER 32
#endif
#define MAX_PDATA_SIZE (RACOM_RX_BUFFER-4)

//-----TP Options----------

//-----General Options-----
#define TIMEOUT 500	//ms



#endif
