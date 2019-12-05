import face_recognition as fr
import numpy
import cv2

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

print("HIT");

capture = cv2.VideoCapture(0)
count = 0

# driver loop
while (1):
    #get frame
    ret, frame = capture.read()
    multiplier = 3
    faster_frame = cv2.resize(frame, (0,0), fx=1/multiplier, fy=1/multiplier)
    
    #processing in rgb for facial recognition
    rgb = faster_frame[:, :, [2, 1, 0]]
    
    if count % 4 == 0:
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
        cv2.imshow('surveil', frame)
    
    if count > 1000000:
        count = 0
    else:
        count+=1
    
    if cv2.waitKey(1) == 27:
        break

# on end
capture.release()
cv2.destroyAllWindows()
