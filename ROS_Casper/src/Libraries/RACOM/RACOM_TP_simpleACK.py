import sys
from RACOM_TP import RACOM_TP
from random import randint
from datetime import datetime


def test(s):
    data = range(s)
    cmd = 1
    sys.stdout.write("Test " + str(s) + " :\t")
    for i in data:
        data[i] = randint(0,255)
    
    sys.stdout.write("Sending\t")

    RacomTP.send(cmd,data)
    while RacomTP.available() != 1 :
        continue
    reply = RacomTP.read()
    #print reply

    sys.stdout.write("\t\tReceived\t")#print data
    if reply == data:
        print "SUCCESS"
        return 1
    else:
        print "FAIL reply :",type(reply)
        return 0

print "RACOM TRANPORT LAYER TEST"

RacomTP = RACOM_TP("UART")

payload_size = 255
N = 10

ok = 0
ko = 0

payload_size = int(raw_input("Enter payload size: ") or "128")
N = int(raw_input("Enter number of tests:") or "100")

t0 = datetime.now()
for i in range(N):
    tmp = test(payload_size)
    if tmp != 1:
        ko+=1
    else:
        ok+=1
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

