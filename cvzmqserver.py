#import time
import zmq
import cv2

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://:5555")
#socket.bind("tcp://35.40.127.161:5555")
cap = cv2.VideoCapture(0)
#sleep(2)

frame_counter = 0
topic = 'opencv'
while True:
    frame_counter += 1
    ret, frame = cap.read()
    socket.send_string(topic, zmq.SNDMORE)
    socket.send_pyobj(frame)
    print('Sent frame {}'.format(frame_counter))