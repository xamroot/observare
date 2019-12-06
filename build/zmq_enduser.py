#import time
import zmq
import cv2

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://0.0.0.0:5553")
#socket.connect("tcp://35.40.127.161:5555")
socket.setsockopt(zmq.SUBSCRIBE, b'opencv')
#sleep(2)
print("connection made")

frame_counter = 0
frame = b""
while True:
	if frame_counter % 2 == 0:
		topic = socket.recv_string()
		print(type(topic))
		print("post")
		frame = socket.recv_pyobj()
	cv2.imshow('Image', frame)
	cv2.waitKey(1)

	print('Received frame number {}'.format(frame_counter))
	frame_counter += 1