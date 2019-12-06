#import time
import zmq
import cv2
import face_recognition as fr

#create encodings for smaller versions of images, save them in array
aaron = fr.load_image_file("aaron_sm.jpg")
a = fr.face_encodings(aaron)[0]
bhuse = fr.load_image_file("bhuse.jpg")
b = fr.face_encodings(bhuse)[0]
camaal = fr.load_image_file("camaal_sm.jpg")
c = fr.face_encodings(camaal)[0]
kelly = fr.load_image_file("kelly_sm.jpg")
k = fr.face_encodings(kelly)[0]
maxt = fr.load_image_file("max_sm.jpg")
m = fr.face_encodings(maxt)[0]
encodings = [a, b, c, k, m]

print("encodings finished!")

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://0.0.0.0:5555")
#socket.bind("tcp://35.40.127.161:5555")
cap = cv2.VideoCapture(0)

print("server set up")

frame_counter = 0
topic = 'opencv'
frame = b""
while True:
	# set up the frame
	ret, frame = cap.read()
	multiplier = 4
	faster_frame = cv2.resize(frame, (0,0), fx=1/multiplier, fy=1/multiplier)
	rgb = faster_frame[:, :, [2, 1, 0]] #processing in rgb for facial recognition

	if frame_counter % 2 == 0:
		locations = fr.face_locations(rgb)
		face_names = []

		if locations:
			new_faces = fr.face_encodings(rgb, locations)
			#add for loop for new faces
			for new_face in new_faces:
				matches = fr.compare_faces(encodings, new_face)

				if True in matches:
					match_index = matches.index(True)
					if match_index == 0: #aaron
						face_names.append("Aaron")
					elif match_index == 1:
						face_names.append("Professor Bhuse")
					elif match_index == 2:
						face_names.append("Camaal")
					elif match_index == 3:
						face_names.append("Kelly")
					elif match_index == 4:
						face_names.append("Max")
					else:
						face_names.append("Stranger")

		for (top, right, bottom, left), name in zip(locations, face_names):
			#draw box around each face in blue
			frame = cv2.rectangle(frame, (left*multiplier, top*multiplier), (right*multiplier, bottom*multiplier), (255, 0, 0), 2)
			font = cv2.FONT_HERSHEY_SIMPLEX
			#add name in white to frame
			frame = cv2.putText(frame, name, (left*multiplier, bottom*multiplier), font, 1.0, (255, 255, 255), 1)


		#we would print the frame here, but we send it to server
		socket.send_string(topic, zmq.SNDMORE)
		print(topic)
		socket.send_pyobj(frame)
		print(frame)
	cv2.imshow('surveil', frame)

	print('Sent frame {}'.format(frame_counter))
	frame_counter += 1

cap.release()
cv2.destroyAllWindows()
