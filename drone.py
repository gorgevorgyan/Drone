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

@sio.on('states')
def states():
    while True:
        sio.emit('toweb',{'height': random.randrange(0,200),
        		 		  'speed': random.randrange(0,200),
        		          'battery': random.randrange(0,200),
        		          'acceleration':{'x':0,'y':0,'z':0},
        		          'gyroscope':{'x':0,'y':0,'z':0},
        		 })
        time.sleep(0.5)

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:5901/')
sio.wait()










