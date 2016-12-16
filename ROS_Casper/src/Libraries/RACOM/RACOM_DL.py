#!/usr/bin/env python

import logging
import RACOM_PHY
from datetime import datetime
from time import sleep


class RACOM_DL(object):
    # Com properties
    _TIMEOUT = 0.5
    #Frame properties
    _STX = 0x02  # start

    #SM variables
    _t0 = 0
    _state = 0
    _packet = []
    _pSize = 0
    _cnt = 0
    _available = 0

    MAX_PDATA_SIZE = 60
    
    def __init__(self,interfaceName):
        """
        Constructor of the Framing class
        """
        self.baudrate = 115200
        self.logger = logging.getLogger(__name__)
        if interfaceName == "UART":
            self.RacomPHY = RACOM_PHY.UART(self.baudrate,self._TIMEOUT)
        elif interfaceName == "I2C":
            self.RacomPHY = RACOM_PHY.I2C(8)
        
    def formatPacket(self, packet):
        
        frame = []
        frame.append(self._STX)
        frame.append((len(packet)<<2) + (packet[0] & 0b11))

        ##DATA
        for i in range(1, len(packet), 1):
            if type(packet[i]) is int:
                frame.append(packet[i])
            else:
                frame.append(ord(packet[i]))
        return frame

    def send(self,packet):
        frame = self.formatPacket(packet)
        self.RacomPHY.write(frame)
		sleep(0.5)

    def read(self):
        if self._available == 1:
            self._available = 0
            return self._packet
        else:
            return 0

    def pSize(self):
        return self._pSize
        
    def available(self):
        if(self.readSM()==-1):
            return -1
        return self._available
    
    def readSM(self):
        #States
        _WAITING_STATE = 0
        _START_STATE = 1
        _WAIT_DATA_STATE = 2

        if self._state is _WAITING_STATE:
            byte = []
            while self.RacomPHY.available() != 0 :
                byte = self.RacomPHY.read()
                if len(byte) == 0:
                    return 0
                else:
                    byte=byte[0]
                if byte is self._STX:
                    self._cnt = 0
                    break
                if self.RacomPHY.available() == -1 :
					break
            if byte is self._STX :
                    self._state = _START_STATE

        elif self._state is _START_STATE:
            self._t0 = datetime.now()
            if self.RacomPHY.available() > 0 and self._available == 0:
                self._packet = []
                self._pSize = self.RacomPHY.read()[0]
                self._pFlags = self._pSize & 0b11
                self._pSize = self._pSize >> 2
                self._packet.append(self._pFlags)
                self._cnt = 1
            elif self.RacomPHY.available() != 0 and self._available == 0:
                self._packet = []
                try:
                    self._pSize = self.RacomPHY.read()[0]
                except:
                    return 0
                self._pFlags = self._pSize & 0b11
                self._pSize = self._pSize >> 2
                self._packet.append(self._pFlags)
                self._cnt = 1
            if self._cnt == 1:
                self._state = _WAIT_DATA_STATE
            elif (datetime.now()-self._t0).total_seconds() >= self._TIMEOUT :
                self._state = _WAITING_STATE
                return -1   
                

        elif self._state is _WAIT_DATA_STATE:
            while self.RacomPHY.available() > 0 and self._cnt < self._pSize:
                self._packet[len(self._packet):]=self.RacomPHY.read()
                self._cnt+=1
            if self.RacomPHY.available() == -1 and self._cnt < self._pSize:
                self._packet[len(self._packet):]=self.RacomPHY.readBytes(self._pSize-1)
                self._cnt+=self._pSize-1
            if (datetime.now()-self._t0).total_seconds() >= self._TIMEOUT :
                self._state = _WAITING_STATE
                return -1
            elif self._cnt == self._pSize :
                self._available = 1
                self._state = _WAITING_STATE
                return 1
        
        return 0