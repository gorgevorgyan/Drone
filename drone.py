import socketio
import time
import random

sio = socketio.Client()
@sio.event
def connect():
    print('connection established')
    sio.emit('hello')
@sio.on('todrone')
def dronid(*args):
    print(args)

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
    while True:
        sio.emit('toweb',{'height': str(random.randrange(0,200)),
        		 		  'speed': str(random.randrange(0,200)),
        		          'battery': str(random.randrange(0,200)),
                          'lx':random.randrange(-10,10),
                          'ly':random.randrange(-10,10),
        		          'acceleration':{'x':str(0),'y':str(0),'z':str(0)},
        		          'gyroscope':{'x':str(0),'y':str(0),'z':str(0)},

        		 })
        time.sleep(0.5)

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('https://airboss.cf/')
sio.wait()










