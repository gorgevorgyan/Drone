from flask import Flask, url_for, render_template, request, redirect, session
from flask_socketio import SocketIO, emit
from flask import jsonify
import random
import json
lx=0
ly=0
app = Flask(__name__)
app.secret_key = "123"
socketio = SocketIO(app)



@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        try:
            if name=='pilot' and passw=='pilot1234':
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))
        except:
            return redirect(url_for('login'))

@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('home'))
@socketio.on('hello')
def welcome():
	print('Drone connected!')
	socketio.emit('states')

@socketio.on('fullRight')
def fullRight():
    socketio.emit('fullRight')

@socketio.on('fullLeft')
def fullLeft():
    socketio.emit('fullLeft')

@socketio.on('stopRotate')
def stopRotate():
    socketio.emit('stopRotate')

@socketio.on('home')
def home():
    socketio.emit('home')

@socketio.on('states')
def turn_right(*states):
	socketio.emit('todrone',states)

@socketio.on('config')
def conf(*config):
    socketio.emit('config',config)

@socketio.on('toweb')
def give(*args):
    global lx
    global ly
    lx=args[0]['lx']
    ly=args[0]['ly']
    #print(lx)
    socketio.emit('toweb',args)
@app.route("/location", methods=['GET', 'POST'])
def location():
    print(lx)
    return jsonify({"geometry": {"type": "Point", "coordinates": [lx, ly]}, "type": "Feature", "properties": {}})
if __name__ == '__main__':
	print('Started')
	socketio.run(app, port=9999)
