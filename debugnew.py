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

with open("face_encoding.txt", "w") as file:
    file.write(' '.join(map(str, face_encoding)) + "\n")
