from RACOM_DL import RACOM_DL
from math import ceil

class RACOM_TP :
	_data = []
	_dSize = 0
	_cmd=0
	
	RacomDL = RACOM_DL("I2C")
	
	def __init__(self,interfaceName):
		RacomDL=RACOM_DL(interfaceName)
	
	def available(self):
		return self.readSM()

	def send(self,cmd,data):
		
		if len(data) == 0:
			nPacket = 1;
		else:
			nPacket = int(ceil(len(data)/float(self.RacomDL.MAX_PDATA_SIZE)));
		
		packet = range(len(data)+2)
		
		if nPacket == 1:
			packet[0]=0b00
		else:
			packet[0]=0b01
		
		packet[1]=cmd
		for i in range(nPacket):
			j=0
			while (j <self.RacomDL.MAX_PDATA_SIZE) and (i*self.RacomDL.MAX_PDATA_SIZE+j)<len(data):
				packet[j+2]=data[i*self.RacomDL.MAX_PDATA_SIZE+j]
				j+=1
			del packet[j+2:]
			self.RacomDL.send(packet)
			code = self.RacomDL.available()
			while code !=1:
				if code <0:
					return code
				code = self.RacomDL.available()
			
			reply = self.RacomDL.read()
			checkSize = reply[2]+(reply[3]<<8)
			if checkSize!=len(packet)-2+i*60:
				return reply[1]
			packet[0]=0b11
			if(i==nPacket-2):
				packet[0]=0b10
		return nPacket
	
	def read(self):
		tmp = self._data
		self._data = []
		self._dSize = 0
		self._available = 0
		return tmp
	
	def cmd(self):
		return self._cmd
	
	def readSM(self):
		okReply = [0,0,0,0]
		if self.RacomDL.available()>0:
			pSize = self.RacomDL.pSize()
			tmp=self.RacomDL.read()
			pFlags = tmp[0]&0b11
			self._cmd = tmp[1]
			s = self._dSize+pSize -2
			okReply[2] = s&0xFF
			okReply[3] = ((s&0xFF00)>>8)
			
			if pFlags == 0b00:
				self._dsize = 0
				self._data = []
				for i in range(2,len(tmp)):
					self._data.append(tmp[i])
				self._dSize+=pSize-2
				self._available = 1
				self.RacomDL.send(okReply)
				return 1
			elif pFlags == 0b01:
				self._dsize = 0
				self._data = []
				for i in range(2,len(tmp)):
					self._data.append(tmp[i])
				self._dSize+=pSize-2
				self._available = 0
				self.RacomDL.send(okReply)
				return 0
			elif pFlags == 0b11:
				for i in range(2,len(tmp)):
					self._data.append(tmp[i])
				self._dSize+=pSize-2
				self._available = 0
				self.RacomDL.send(okReply)
				return 0
			elif pFlags == 0b10:
				for i in range(2,len(tmp)):
					self._data.append(tmp[i])
				self._dSize+=pSize-2
				self._available = 1
				self.RacomDL.send(okReply)
				return 1
		else:
			return 0