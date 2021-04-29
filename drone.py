import socketio
import time
import random
from numpy import interp
import os

hard = 0    #set 0 if you are testing only software
gsm = 1     #set 0 if you are Gor :)

if hard: 
    import pigpio
    pi = pigpio.pi() 

if gsm:
    import serial
    port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.3)
    port.write(b"AT+DDET=1,1000,0,0;\r")
    rcv = port.read(10).strip()
    print(rcv)

sio = socketio.Client()

motors = [
[21, 13],
[19, 16]]

motor_speed = [[900, 900], [900, 900]]

last_dtmf = 0
lost_state = 0

def get_dtmf():
    global last_dtmf
    rcv = port.read(10).strip().decode()
    if "DTMF" in rcv:
        try:
            last_dtmf = int(rcv.split()[1])
            print(last_dtmf)
        except:
            print("SMTH is wrong")

def update_motor_speeds(start=True):
    if hard:
        if start:
            for i in range(2):
                for j in range(2):
                    pi.set_servo_pulsewidth(motors[i][j], motor_speed[i][j])
            
        else:

            for k in (900, 1000):
                for i in motors:
                    for j in i:
                        pi.set_servo_pulsewidth(j, k)

update_motor_speeds(start=False)

@sio.event
def connect():
    print('connection established')
    sio.emit('hello')

@sio.on('todrone')
def dronid(*args):
    data = args[0]
    print(data)
    motor_speed[0][0] = interp((float(data["z"]) + ( (float(data["X_config"]) * (float(data["x"]) * -1) - float(data["Y_config"]) * float(data["y"])) )), [0, 100], [1000, 2000]) * float(data['m1']) / 100
    motor_speed[0][1] = interp((float(data["z"]) - ( (float(data["X_config"]) * (float(data["x"]) * -1) + float(data["Y_config"]) * float(data["y"])) )), [0, 100], [1000, 2000]) * float(data['m2']) / 100
    motor_speed[1][0] = interp((float(data["z"]) + (float(data["X_config"]) * (float(data["x"]) * -1) + float(data["Y_config"]) * float(data["y"]))), [0, 100], [1000, 2000]) * float(data['m3']) / 100
    motor_speed[1][1] = interp((float(data["z"]) + ( (float(data["Y_config"]) * float(data["y"]) - float(data["X_config"]) * (float(data["x"]) * -1) ) )), [0, 100], [1000, 2000]) * float(data['m4']) / 100
    print(motor_speed)

@sio.on('config')
def dronid(*config):
    print(config)

@sio.on('fullRight')
def fullRight():
    print('fullRight') 

@sio.on('home')
def home():
    print('home')

@sio.on('fullLeft')
def fullLeft():
    print('fullLeft')

@sio.on('stopRotate')
def stopRotate():
    print('stopRotate')

@sio.on('states')
def states():
    global last_dtmf
    global lost_state
    while True:
        sio.emit('toweb',{'height': str(random.randrange(0,200)),
        		 		  'speed': str(random.randrange(0,200)),
        		          'battery': str(random.randrange(0,200)),
                          'lx':random.randrange(-10,10),
                          'ly':random.randrange(-10,10),
        		          'acceleration':{'x':str(0),'y':str(0),'z':str(0)},
        		          'gyroscope':{'x':str(0),'y':str(0),'z':str(0)},

        		 })
        if hard:
            update_motor_speeds()
        if gsm:
            if lost_state == 1:
                if last_dtmf != 0:
                    if last_dtmf == 1:
                        print("Sending message")
                    elif last_dtmf == 2:
                        print("Going down")
                    elif last_dtmf == 3:
                        print("Auto Home")
                    else:
                        print("Wrong Command")
                    last_dtmf = 0
        get_dtmf()
        time.sleep(0.3)

@sio.event
def disconnect():
    global lost_state
    if gsm:
        print('Connection Lost Calling')
        port.write(b'ATD+37494221203;\r')
        rcv = port.read(10).strip()
        print(rcv)
        lost_state = 1
    else:
        print("Connection lost without gsm")

sio.connect('https://airboss.cf/')
sio.wait()










