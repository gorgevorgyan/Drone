from flask import Flask, render_template, Response
from flask_cors import CORS, cross_origin
import cv2
import socket
import sys
import pickle
import numpy as np
import struct ## new
import zlib

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5901/"}})
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route('/')
def index():
    return "Sorry You can not fly"

host_name  = socket.gethostname()
HOST=socket.gethostbyname(host_name)
PORT=9999
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(10)
print('Socket now listening')
def gen():
    while True:
        conn,addr=s.accept()
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
        data = b""
        payload_size = struct.calcsize(">L")
        print("payload_size: {}".format(payload_size))
        while True:
            while len(data) < payload_size:
                #print("Recv: {}".format(len(data)))
                data += conn.recv(4096)
            #print("Done Recv: {}".format(len(data)))
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            #print("msg_size: {}".format(msg_size))
            while len(data) < msg_size:
                data += conn.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame=pickle.loads(frame_data)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            #print(frame)
            out.write(frame)
        # rval, frame = vc.read()
            cv2.imwrite('t.jpg', frame)
   
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')

                  
@app.route('/video_feed')
@cross_origin()
def video_feed():
    print('araaaaaaaaaaah')
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5900)




