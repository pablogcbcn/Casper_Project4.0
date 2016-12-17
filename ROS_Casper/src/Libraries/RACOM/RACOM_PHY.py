#!/usr/bin/env python

import serial

import smbus
import pigpio
import logging
from time import sleep



class UART(object):

    def __init__(self, baudrate, timeout=0.001):
        """
        Constructor of the UART class
        Open the serial port

        Keyword arguments:
        baudrate -- speed of the UART (default 115200)
        timeout -- timeout is there to pass a read even if all the x char
        haven't arrived (default 0.05s)
        """

        self.logger = logging.getLogger(__name__)
        self.__baudrate = baudrate
        self.__timeOut = timeout
        self.connection = None

        self.open()
        self.connection.flushInput()
        self.connection.flushOutput()

    def open(self):
        """
        Open the serial port
        """
        try:
            if self.connection == None or self.connection.isOpen() is False:
                self.connection = serial.Serial("/dev/ttyAMA0",  self.__baudrate, 8, serial.PARITY_NONE, serial.STOPBITS_ONE, xonxoff=0, rtscts=0, timeout=self.__timeOut)
        except serial.SerialException:
            self.logger.error("Impossible to open the serial port", exc_info=True)

    def close(self):
        """
        Close the serial port
        """
        try:
            if self.connection.isOpen() is True:
                self.connection.close()
        except serial.SerialException:
            self.logger.error("Impossible to close the serial port", exc_info=True)

    def write(self, data):
        for i in range(0, len(data), 1):
            data[i] = data[i] & 0xFF
        data = bytearray(data)

        try:
            self.connection.write(data)
        except serial.SerialException:
            self.logger.warn("Impossible to send the data through serial", exc_info=True)

    def read(self):
        data = 0
        try:
            data = self.readBytes(1)
        except:
            pass
        return data

    def readBytes(self,len):
        data = []
        if len == 0:
            return data
        try:
            data = [ord(x) for x in self.connection.read(len)]
        except:
            pass
        return data
    
    def available(self):
        data = 0
        try:
            data = self.connection.inWaiting()
        except:
            pass
        return data

class I2C(object):
	def __init__(self, slaveAdress):
		self.bus_number = 1
		self.slaveAdress = slaveAdress
		self.open()
		self._RXBuffer = []
		
	def open(self):
		smbus.SMBus(1).close
		try:
			self.bus = smbus.SMBus(1)
		except:
			self.logger.error("Impossible to open the I2C bus")
			
	def write(self, data):
		if type(data) == int:
			data = [data]
		try:
			print data
			self.bus.write_i2c_block_data(self.slaveAdress,data[0],data[1:])
		except:
			pass
	
	def read(self):
		data=[]
		data=self.readBytes(1)
		return data
		
	def readBytes(self,len):
		data = []
		if len == 0:
			return []
		try:
			data = self.bus.read_i2c_block_data(self.slaveAdress,len)
		except:
			sleep(0.005)
			print "failed"
			return []
		if type(data) is int:
			return [data]
		else:
			return data[:len]

	def available(self):
		return -1