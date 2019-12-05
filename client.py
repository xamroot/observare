import cv2
import io
import socket
import struct
import time
import pickle
import zlib

socket_details = ('0.0.0.0', 5001)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(socket_details)
print("hit")
client_socket.close()

'''
connection = client_socket.makefile('wb')

cam = cv2.VideoCapture(0)
img_counter = 0
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while 1:
    ret, frame = cam.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    data = pickle.dumps(frame, 0)
    size = len(data)
    print("{}: {}".format(img_counter, size))
    client_socket.sendall(struct.pack("<L", size) + data)
    img_counter += 1

cam.release() '''