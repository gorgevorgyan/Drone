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
        sio.emit('toweb',{'height': random.randrange(0,200)})
        time.sleep(0.5)

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://cuadro.ml:5901')
sio.wait()
