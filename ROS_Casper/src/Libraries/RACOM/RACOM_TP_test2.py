import sys
from RACOM_TP import RACOM_TP
from random import randint

RacomTP = RACOM_TP("UART")
testSize = randint(0,10)
cmd = 1
data = range(testSize)
data = range(40)
print data

print RacomTP.send(cmd,data)

while(RacomTP.available()<=0):
    continue

print RacomTP.read()
