import socketio
import time
import random
from numpy import interp
import os    
import serial


hard = 1    # set 0 if you are testing only software
gsm = 1     # set 0 if you are Gor :)
gyro = 1    # set 0 if you don`t have gyro
gps =  1    # set 0 if you don`t have gps

GSM_PORT = "/dev/ttyUSB0"
GPS_PORT = "/dev/ttyS0"
GSM_BAUDRATE = 9600
GPS_BAUDRATE = 9600
SERIAL_TIMEOUT = 0.3
GYRO_ADRESS = 0x68
BATTERY_LEVEL = 95
GPS_FILE_NAME = "gps.txt"

if hard: 
    import pigpio
    pi = pigpio.pi() 

if gsm:
    gsm_port = serial.Serial(GSM_PORT, baudrate=GSM_BAUDRATE, timeout=SERIAL_TIMEOUT)
    gsm_port.write(b"AT+DDET=1,1000,0,0;\r")
    rcv = gsm_port.read(10).strip()
    print(rcv)

if gyro:
    from mpu6050 import mpu6050
    sensor = mpu6050(GYRO_ADRESS)

if gps:
    gps_port = serial.Serial(GPS_PORT, baudrate=GPS_BAUDRATE, timeout=SERIAL_TIMEOUT)
    print("GPS Started")

sio = socketio.Client()

motors = [
[21, 13],
[19, 16]]

motor_speed = [[900, 900], [900, 900]]

last_dtmf = 0
lost_state = 0

def get_dtmf():
    global last_dtmf
    rcv = gsm_port.read(10).strip().decode()
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
        if gyro:
            gyro_data = sensor.get_gyro_data()
        else: 
            gyro_data = { "x": 0, "y": 0, "z" : 0}
        sio.emit('toweb',{'height' : str(random.randrange(0, 200)),
        		 		  'speed' : str(random.randrange(0, 200)),
        		          'battery' : BATTERY_LEVEL,
                          'lx' : float(open(GPS_FILE_NAME).readline().split("\n")[0].strip().split("|")[0]),
                          'ly' : float(open(GPS_FILE_NAME).readline().split("\n")[0].strip().split("|")[1]),
        		          'acceleration' : { 'x' : str(0), 'y' : str(0), 'z' : str(0)},
        		          'gyroscope' : { 'x' : str(round(gyro_data["x"], 2)), 'y' : str(round(gyro_data["y"], 2)), 'z' : str(round(gyro_data["y"], 2))},
                           })
        if hard:
            update_motor_speeds()
        if gsm:
            get_dtmf()
            if lost_state == 1:
                if last_dtmf != 0:
                    if last_dtmf == 1:
                        print("Sending message")
                        gsm_port.write(b'AT+CREC=4,"C:\\User\\mess.amr",1,100 \r')
                        time.sleep(0.1)
                        gsm_port.write(b'AT+CMGS="+37494221203"\r')
                        print(gsm_port.read(50).strip())
                        time.sleep(0.2)
                        gsm_port.write(('DRONE STATE \n Latitude: ' + str(open(GPS_FILE_NAME).readline().split("\n")[0].strip().split("|")[0]) + 
                                        ' \n Longitude: ' + str(open(GPS_FILE_NAME).readline().split("\n")[0].strip().split("|")[1]) + ' \n ' + 
                                        ' Battery Level: ' + str(BATTERY_LEVEL) + ' \r').encode())
                        print(gsm_port.read(50).strip())
                    elif last_dtmf == 2:
                        print("Going down")
                        gsm_port.write(b'AT+CREC=4,"C:\\User\\down.amr",1,100 \r')
                        if hard: drone_get_off()
                    elif last_dtmf == 3:
                        print("Auto Home")
                        gsm_port.write(b'AT+CREC=4,"C:\\User\\auto.amr",1,100 \r')
                        if hard: drone_auto_home()
                    elif last_dtmf == 4:
                        print("Get battery level")
                        gsm_port.write(b'AT+CREC=4,"C:\\User\\bat.amr",1,100 \r')
                        time.sleep(1.5)
                        gsm_port.write(b'AT+CREC=4,"C:\\User\\95.amr",1,100 \r')
                    else:
                        print("Wrong Command")
                    last_dtmf = 0
        if gps: getPositionData(gps_port)
        time.sleep(0.3)

def drone_get_off():
    global motor_speed
    new_speeds = list(range(900, int(motor_speed[0][0])))
    new_speeds.reverse()
    for speed in new_speeds:
        for i in range(0, 2): 
            for j in range(0, 2):
                motor_speed[i][j] = speed
        time.sleep(0.2) 

def drone_auto_home():
    global motor_speed
    new_speeds = list(range(900, int(motor_speed[0][0])))
    new_speeds.reverse()
    for speed in new_speeds:
        for i in range(0, 2): 
            for j in range(0, 2):
                motor_speed[i][j] = speed
        time.sleep(0.2) 

def formatDegreesMinutes(coordinates, digits):
    
    parts = coordinates.split(".")

    if (len(parts) != 2):
        return coordinates

    if (digits > 3 or digits < 2):
        return coordinates
    
    left = parts[0]
    right = parts[1]
    degrees = str(left[:digits])
    minutes = str(right[:3])

    return degrees + "." + minutes

def getPositionData(gps):
    data = gps.readline().decode()
    message = data[0:6]
    if (message == "$GPRMC"):
        parts = data.split(",")
        if parts[2] == 'V':
            #print("GPS receiver warning")
            pass
        else:
            longitude = formatDegreesMinutes(parts[5], 3)
            latitude = formatDegreesMinutes(parts[3], 2)
            open(GPS_FILE_NAME, "w").write(str(latitude) + "|" + longitude)
            print( "Your position: lon = " + str(longitude) + ", lat = " + str(latitude))
    else:
        # Handle other NMEA messages and unsupported strings
        pass

@sio.event
def disconnect():
    global lost_state
    if gsm:
        print('Connection Lost Calling')
        gsm_port.write(b'ATD+37494221203;\r')
        rcv = gsm_port.read(10).strip()
        #time.sleep(5) 
        #port.write(b'AT+CREC=4,"C:\\User\\lost.amr",1,100 \r')
        #rcv = port.read(15).strip().decode()
        print(rcv)
            
        lost_state = 1
    else:
        print("Connection lost without gsm")

sio.connect('https://airboss.cf/')
sio.wait()










