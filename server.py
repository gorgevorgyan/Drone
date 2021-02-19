from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@socketio.on('hello')
def welcome():
	print('Drone connected!')
	socketio.emit('states')

@socketio.on('right')
def turn_right():
	socketio.emit('right')

@socketio.on('up')
def turn_up():
	socketio.emit('up')

@socketio.on('left')
def turn_left():
	socketio.emit('left') 

@socketio.on('down')
def turn_down():
	socketio.emit('down')

@socketio.on('toweb')
def give(*args):
	socketio.emit('toweb',args)

if __name__ == '__main__':
	print('Started')
	socketio.run(app, port=8000)