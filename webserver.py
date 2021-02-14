from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('Height')
def test_connect(*args):
    print(args)
    #emit('Drone_ID', {'data': 'h'})

@socketio.on('connect')
def test_connect():
    emit('connect',"Connected to server!")

if __name__ == '__main__':
    socketio.run(app, port=8000)