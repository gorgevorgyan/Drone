import serial
import os, time
 
# Enable Serial Communication
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
 
# Transmitting AT Commands to the Modem
# '\r\n' indicates the Enter key

port.write(b"AT+DDET=1,1000,0,0;\r")
rcv = port.read(10).strip()
print(rcv)
port.write(b'ATD+37494221203;\r')
rcv = port.read(10).strip()
print(rcv)
while 1: 
#	port.write('AT'+'\r\n')
	rcv = port.read(10).strip()	
	print(rcv)
