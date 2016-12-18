import sys
from RACOM_TP import RACOM_TP
from random import randint
from datetime import datetime
from time import sleep

def test(s):
	data = range(s)
	cmd = 1

	#for i in data:
	#	data[i] = randint(0,255)
		
	code = RacomTP.send(cmd,data)
	if code < 0:
		print code
		return 0
	#sleep(0.01)
		


	_t0 = datetime.now()
	while True :
		code=RacomTP.available()
		if code is -1 or (datetime.now()-_t0).total_seconds() > RacomTP._TIMEOUT:
			return 0
		elif code is 1:
			break
	reply = RacomTP.read()
	if reply == data:
		return 1
	else:
		return 0


payload_size = 255
N = 10

ok = 0
ko = 0

print "RACOM TRANPORT LAYER TEST 01"
iface = raw_input("Interface to test: ") or "I2C"
payload_size = int(raw_input("Enter payload size: ") or "16")
N = int(raw_input("Enter number of tests:") or "100")
sys.stdout.write("Testing: ")
print iface,"interface"
RacomTP = RACOM_TP(iface)

t0 = datetime.now()

for i in range(N):
	tmp = test(payload_size)
	if tmp != 1:
		ko+=1
	else:
		ok+=1
	#sleep(0.02)
	sys.stdout.write("\t %d %% complete         \r" % int((i+1.0)/(N)*100))
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

