# #Importing Modules
# import socket, threading
# drone_id ="1" 
# server_host =socket.gethostname()
# server_port = 9999
# #socket initialization
# drone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #connecting drone to server     
# drone.connect((server_host, server_port))                             
# def receive():
#     while True:                                                 
#         try:
#             message = drone.recv(1024).decode('ascii')
#             if message == 'Id':
#                 drone.send(drone_id.encode('ascii'))
#             else:
#                 print(message)
#         except:                                                 
#             print("An error occured!")
#             drone.close()
#             break
# def write():
#     while True:                                               
#         message = "ok"
#         drone.send(message.encode('ascii'))

# receive_thread = threading.Thread(target=receive)               
# receive_thread.start()
# write_thread = threading.Thread(target=write)                  
# write_thread.start()
from socketIO_client import SocketIO, LoggingNamespace

# def on_bbb_response(*args):
#     print('on_bbb_response', args)

def on_connect(response):
    print(response)

with SocketIO('localhost', 8000, LoggingNamespace) as socketIO:
    socketIO.emit('connect')
    socketIO.on('connect', on_connect)
    while True:
        socketIO.emit('Height', {'height': '15'})
    socketIO.wait_for_callbacks(seconds=0.1)