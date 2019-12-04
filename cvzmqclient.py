#import time
import zmq
import cv2

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
#socket.connect("tcp://35.40.127.161:5555")
socket.setsockopt(zmq.SUBSCRIBE, b'opencv')
#sleep(2)

frame_counter = 0
while True:
    frame_counter += 1
    topic = socket.recv_string()
    frame = socket.recv_pyobj()
    cv2.imshow('Image', frame)
    cv2.waitKey(1)

    print('Received frame number {}'.format(frame_counter))