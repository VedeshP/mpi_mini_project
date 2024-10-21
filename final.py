# Import necessary libraries
import cv2  # OpenCV library for computer vision tasks
import numpy as np  # NumPy for numerical operations
import mediapipe as mp  # MediaPipe for face detection
from cvzone.FaceDetectionModule import FaceDetector  # Face detection module from CVZone
from cvzone.SerialModule import SerialObject  # Serial communication module from CVZone

# Initialize the webcam for video capture (default camera at index 0)
cap = cv2.VideoCapture(0)

# Create a FaceDetector object to detect faces in the video stream
detector = FaceDetector()

# Initialize the serial object to communicate with Arduino via the specified COM port
# Make sure the COM port matches the one assigned to the Arduino on your system
# Vraj COM7 - Vedesh COM3
arduino = SerialObject('COM3')

# Load the reference image of the known face from the specified path
known_face_image = cv2.imread(r"C:\Users\HP\Downloads\known_face.jpg")

# Convert the known face image from BGR (OpenCV default) to grayscale
# Face recognition models often work better with grayscale images
known_face_image_gray = cv2.cvtColor(known_face_image, cv2.COLOR_BGR2GRAY)

# Initialize the LBPH (Local Binary Patterns Histogram) face recognizer
# This algorithm is effective for recognizing individual faces
known_face_encoding = cv2.face.LBPHFaceRecognizer_create()
# The above is from opencv-contrib-python
# known_face_encoding = cv2.face.createLBPHFaceRecognizer()

# Train the face recognizer with the known face image
# The label '0' is associated with the known face during training
known_face_encoding.train([known_face_image_gray], np.array([0]))

# Start an infinite loop to continuously read frames from the webcam
while True:
    # Read a frame from the webcam (returns success flag and the frame)
    success, img = cap.read()

    # Convert the current frame from BGR to RGB for compatibility with MediaPipe's detection
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect faces in the current frame using the FaceDetector object
    # 'dBoxes' contains information about detected faces (bounding boxes)
    img, dBoxes = detector.findFaces(img)

    # Check if at least one face is detected
    if dBoxes:
        # Extract the bounding box of the first detected face
        x, y, w, h = dBoxes[0]['bbox']

        # Crop the face region from the original RGB image using the bounding box coordinates
        face_region = img_rgb[y:y+h, x:x+w]

        # Convert the cropped face region to grayscale for recognition
        face_region_gray = cv2.cvtColor(face_region, cv2.COLOR_RGB2GRAY)

        # Use the trained LBPH face recognizer to predict the label and confidence of the detected face
        label, confidence = known_face_encoding.predict(face_region_gray)

        # Set a threshold for confidence; lower values indicate better matches
        threshold = 100  # Adjust this value based on the quality of recognition

        # If the predicted face matches with confidence below the threshold
        if confidence < threshold:
            arduino.sendData([0, 1])  # Send data to turn OFF the LED (face recognized)
            print("Known face detected. LED OFF!")
        else:
            arduino.sendData([1, 0])  # Send data to turn ON the LED (unknown face)
            print("Unknown face detected. LED ON.")
    else:
        # If no face is detected in the frame, turn ON the LED
        arduino.sendData([1, 0])
        print("No face detected. LED ON.")

    # Display the current frame with detected faces in a window
    cv2.imshow("Video", img)

    # Wait for the 'q' key to be pressed to break the loop and stop the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()