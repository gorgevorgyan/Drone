import cv2
import io
import socket
import struct
import time
import pickle
import zlib
import imutils
import numpy as np
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('45.143.205.46', 6666))
connection = client_socket.makefile('wb')
print("Connected")
cam = cv2.VideoCapture(0)

cam.set(3, 320);
cam.set(4, 240);

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 9]

while True:
    ret, frame = cam.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    result, frame = cv2.imencode('.jpg', frame, encode_param)
#    data = zlib.compress(pickle.dumps(frame, 0))
    data = pickle.dumps(frame, 0)
    size = len(data)


    print("{}: {}".format(img_counter, size))
    client_socket.sendall(struct.pack(">L", size) + data)
    img_counter += 1

cam.release()
