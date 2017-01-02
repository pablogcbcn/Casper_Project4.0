import sys
from RACOM_DL import RACOM_DL
from random import randint
from datetime import datetime
from time import sleep


def test(s):
	data = range(s)
	sys.stdout.flush()
	
	RacomDL.RacomPHY.write(data)
	reply = []
	#sleep(0.01)
	while len(reply) != len(data) :
		if (RacomDL.RacomPHY.available() == -1) :
			reply[len(reply):]=RacomDL.RacomPHY.readBytes(len(data))
		else :
			reply[len(reply):]=RacomDL.RacomPHY.readBytes(RacomDL.RacomPHY.available())

	if reply == data:
		#print "SUCCESS"
		return 1
	else:
		print "FAIL reply :", reply
		return 0

print "RACOM PHYSICAL LAYER TEST 01"



payload_size = 8
N = 10

ok = 0
ko = 0

iface = raw_input("Interface to test: ") or "I2C"
payload_size = int(raw_input("Enter payload size: ") or "8")
N = int(raw_input("Enter number of tests:") or "10")
sys.stdout.write("Testing: ")
print iface,"interface"

RacomDL = RACOM_DL(iface)

t0 = datetime.now()

for i in range(N):
	tmp = test(payload_size)
	if tmp != 1:
		ko+=1
	else:
		ok+=1
	sys.stdout.write("\t %d %% complete         \r" % int((i)/(N-1)*100))
	sys.stdout.flush()
		
t1 = datetime.now()

sys.stdout.write("\r\n")
sys.stdout.write("Robustness test results: \r\n")
sys.stdout.write("Payload size: ")
sys.stdout.write("\t%d\r\n" % payload_size)
sys.stdout.write("N: ")
sys.stdout.write("\t\t%d\r\n" % N)
sys.stdout.write("Time: ")
time = (t1-t0).total_seconds()
sys.stdout.write("\t\t%f\ts\r\n" % time)
sys.stdout.write("Throughput: ")
Thru = (100.0*(ok/float(N)))
sys.stdout.write("\t%f\t%%\r\n" % Thru)
sys.stdout.write("Speed: ")
speed = N*payload_size/time
sys.stdout.write("\t\t%d\t\tBps\r\n" % speed)

