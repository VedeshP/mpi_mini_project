import cv2
import cv2.face
import numpy as np
import mediapipe as mp
from cvzone.FaceDetectionModule import FaceDetector
from cvzone.SerialModule import SerialObject

# Initialize camera, face detector, and Arduino serial communication
cap = cv2.VideoCapture(0)
detector = FaceDetector()
arduino = SerialObject('COM7')  # Set the appropriate COM port

# Load the known face image and convert to grayscale
known_face_image = cv2.imread(r"known_face1.jpg")
known_face_image_gray = cv2.cvtColor(known_face_image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

# Initialize the LBPH face recognizer and train it with the known face
# known_face_encoding = cv2.face.LBPHFaceRecognizer_create()
known_face_encoding = cv2.face.LBPHFaceRecognizer.create()
known_face_encoding.train([known_face_image_gray], np.array([0]))

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB
    img, dBoxes = detector.findFaces(img)

    if dBoxes:
        # Extract face region for recognition
        x, y, w, h = dBoxes[0]['bbox']
        face_region = img_rgb[y:y+h, x:x+w]

        # Convert face region to grayscale
        face_region_gray = cv2.cvtColor(face_region, cv2.COLOR_RGB2GRAY)

        # Predict the face
        label, confidence = known_face_encoding.predict(face_region_gray)

        # Set a threshold for recognition confidence
        threshold = 100  # You may adjust this threshold

        if confidence < threshold:  # If the confidence is below the threshold, it's a match
            arduino.sendData([0, 1])  # Turn ON LED if the specific face is detected
            print("Known face detected. LED OFF!")
        else:
            arduino.sendData([1, 0])  # Turn OFF LED for unknown face
            print("Unknown face detected. LED ON.")
    else:
        arduino.sendData([1, 0])  # Turn OFF LED if no face is detected
        print("No face detected. LED ON.")

    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()