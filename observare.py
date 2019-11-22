import face_recognition as fr
import numpy
import cv2
'''
f = open("encodings.txt")
fstring = f.read()
fstring.replace('[', "")
fstring.replace(']', "")
encodings = fstring.split(',')
f.close()
'''

#bhuse = fr.load_image_file("bhuse.jpg")
#b = fr.face_encodings(bhuse)[0]
camaal = fr.load_image_file("camaal_sm.jpg")
c = fr.face_encodings(camaal)[0]
kelly = fr.load_image_file("kelly_sm.jpg")
k = fr.face_encodings(kelly)[0]
encodings = [c, k]
print(encodings)

print("HIT");
#encodings = [k, c, m, a, b]

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
        
        if locations:
            new_faces = fr.face_encodings(rgb, locations)
            
            #add for loop for new faces
            for new_face in new_faces:
                matches = fr.compare_faces(encodings, new_face)
                if True in matches:
                    match_index = matches.index(True)
                    if match_index ==0:
                        print("Camaal")
                    else:
                        print("Kelly")
        
        #draw box around face
        for (top, right, bottom, left) in locations:
            #x1, y1, x2, y2, = left, top, right, bottom
            frame = cv2.rectangle(frame, (left*multiplier, top*multiplier), (right*multiplier, bottom*multiplier), (255, 0, 0), 2)
            
        
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