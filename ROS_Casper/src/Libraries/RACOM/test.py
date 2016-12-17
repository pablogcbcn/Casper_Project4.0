import sys
import time



sys.stdout.write("\r\n")
sys.stdout.write("Printing Test: \r\n")

for i in range(256):
	time.sleep(0.1)
	print int((i/255.0)*100),"% complete         \r",
	sys.stdout.flush()
sys.stdout.write("\r\n")