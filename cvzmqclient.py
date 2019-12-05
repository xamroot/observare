#import time
import zmq
import cv2

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://35.40.125.58:5555")
print("connected")
#socket.connect("tcp://35.40.127.161:5555")
socket.setsockopt(zmq.SUBSCRIBE, b'opencv')
#sleep(2)

frame_counter = 0
frame = b""
while True:
    if frame_counter % 3 == 0:
        print("after frame counter")
        topic = socket.recv_string()
        print("after topic")
        frame = socket.recv_pyobj()
        frame = cv2.resize(frame, (640, 480))
        cv2.imshow('Image', frame)
        cv2.waitKey(1)

    print('Received frame number {}'.format(frame_counter))
    frame_counter += 1
