from flask import Flask, url_for, render_template, request, redirect, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
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
            if name=='admin' and passw=='admin1234':
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

@socketio.on('states')
def turn_right(*states):
	socketio.emit('todrone',states)
	#print(states)

@socketio.on('toweb')
def give(*args):
	socketio.emit('toweb',args)

if __name__ == '__main__':
	print('Started')
	app.secret_key = "123"
	socketio.run(app, port=8080)
