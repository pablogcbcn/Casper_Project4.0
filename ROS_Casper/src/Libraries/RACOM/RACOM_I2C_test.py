import sys
#from RACOM_TP import RACOM_TP
import RACOM_PHY
from random import randint
from datetime import datetime

RacomPHY = RACOM_PHY.I2C(8)

sent = [4,2,4,2,4,2]

RacomPHY.write(sent)
print RacomPHY.readBytes(6)
print RacomPHY.read()



#bus = smbus.SMBus(1)
#bus.write_byte(8,42)
#data = range(32)
#bus.write_i2c_block_data(8,data[0],data[1:])