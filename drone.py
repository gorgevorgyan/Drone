import socketio
import time
sio = socketio.Client()

@sio.event
def connect():
    print('connection established')
    sio.emit('hello')

@sio.on('right')
def turn_right():
    print('right')

@sio.on('left')
def turn_left():
    print('left')

@sio.on('up')
def turn_up():
    print('up')

@sio.on('down')
def turn_down():
    print('down')

@sio.on('states')
def states():
    while True:
        sio.emit('toweb',{'height': 50})
        time.sleep(0.5)

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:8000')
sio.wait()