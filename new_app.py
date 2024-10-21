import mediapipe as mp
import cv2
import face_recognition
from cvzone.SerialModule import SerialObject

# Load known faces and their encodings
known_face_encodings = []
known_face_names = []

# Add known faces (example)
face_image = face_recognition.load_image_file("known_face1.jpg")
face_encoding = face_recognition.face_encodings(face_image)[0]
known_face_encodings.append(face_encoding)
known_face_names.append("Vedesh")

cap = cv2.VideoCapture(0)
arduino = SerialObject('COM3')

while True:
    success, img = cap.read()
    
    # Convert the image from BGR color (OpenCV format) to RGB color (face_recognition format)
    rgb_frame = img[:, :, ::-1]

    # Find all face locations in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)

    # Proceed only if faces are found
    if face_locations:
        # Find face encodings for each face location
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Check each face found in the frame
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            
            # If a match was found in known_face_encodings
            if True in matches:
                matched_idx = matches.index(True)
                name = known_face_names[matched_idx]
                print(f"Detected: {name}")
                
                # Send signal to Arduino for specific face
                arduino.sendData([0, 1])  # Send data when recognized face is detected
            else:
                print("Unknown face detected")
                arduino.sendData([1, 0])  # Send different data when the face is not recognized

        # Show the video with bounding boxes
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)

    cv2.imshow("Video", img)
    cv2.waitKey(1)



"""Previous Code"""

# import mediapipe as mp
# import cv2
# import face_recognition
# from cvzone.SerialModule import SerialObject

# # Load known faces and their encodings
# known_face_encodings = []
# known_face_names = []

# # Add known faces (example)
# # You can use face_recognition.load_image_file() to load images and face_recognition.face_encodings() to encode them
# face_image = face_recognition.load_image_file("known_face1.jpg")
# face_encoding = face_recognition.face_encodings(face_image)[0]
# known_face_encodings.append(face_encoding)
# known_face_names.append("Vedesh")

# cap = cv2.VideoCapture(0)
# arduino = SerialObject('COM3')

# while True:
#     success, img = cap.read()
    
#     # Convert the image from BGR color (OpenCV format) to RGB color (face_recognition format)
#     rgb_frame = img[:, :, ::-1]

#     # Find all face locations and face encodings in the current frame
#     face_locations = face_recognition.face_locations(rgb_frame)
#     face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

#     # Check each face found in the frame
#     for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#         # See if the face is a match for known faces
#         matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        
#         # If a match was found in known_face_encodings
#         if True in matches:
#             matched_idx = matches.index(True)
#             name = known_face_names[matched_idx]
#             print(f"Detected: {name}")
            
#             # Send signal to Arduino for specific face
#             arduino.sendData([0, 1])  # Send data when recognized face is detected
#         else:
#             print("Unknown face detected")
#             arduino.sendData([1, 0])  # Send different data when the face is not recognized

#     # Show the video with bounding boxes
#     for (top, right, bottom, left) in face_locations:
#         cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)

#     cv2.imshow("Video", img)
#     cv2.waitKey(1)
