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

@socketio.on('states')
def turn_right(*states):
	socketio.emit('todrone',states)
	#print(states)

@socketio.on('toweb')
def give(*args):
	socketio.emit('toweb',args)

if __name__ == '__main__':
	print('Started')
	socketio.run(app, port=5000)
