#import time
import zmq
import cv2
import sys

if (len(sys.argv) < 3):
    print("Usage: python3 zmq_central.py ip listener_port bind_port")
    sys.exit()

ip = sys.argv[1]
port = sys.argv[2]
target = "tcp://" + ip + ":" + port

bind = "tcp://*:" + sys.argv[3]

context = zmq.Context() # set zmq context, unsure of what it does

# initialize socket to accept pi data
pi_handler_socket = context.socket(zmq.SUB)
pi_handler_socket.connect(target)
pi_handler_socket.setsockopt(zmq.SUBSCRIBE, b'opencv')
print("pi facing socket initialized")

# initialize socket to send pi data
enduser_handler_socket = context.socket(zmq.PUB)
enduser_handler_socket.bind(bind)
print("end user facing socket initialized")

# set metadata vars
frame_counter = 0
frame = b""

# driver
while True:
	# handle every third frame
	if frame_counter % 2 == 0:
		topic = pi_handler_socket.recv_string() # recieve topic string data from pi
		print("topic data recieved from pi")
		
		enduser_handler_socket.send_string(topic, zmq.SNDMORE)	# send topic string data to end users
		print("topic data sent to end user")

		frame = pi_handler_socket.recv_pyobj() # recieve frame data from pi
		print("frame data recieved from pi")

		enduser_handler_socket.send_pyobj(frame) # send frame data to enduser
		print("frame data recieved from pi")

	# cv2 wait, ensure of why think its a "sync" thing 
	# (whatever the fuck that means)
	cv2.waitKey(1)

	print('Received frame number {}'.format(frame_counter))
	frame_counter += 1 # increment frame counter
