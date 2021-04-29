import serial
import os, time

# Enable Serial Communication
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)

# Transmitting AT Commands to the Modem
# '\r\n' indicates the Enter key

while 1:
	i = input()
#	print(i)
        #port.write(str(i)+'\r\n')
	port.write(str(i).encode())
	rcv = port.read(30)
	print(rcv)
