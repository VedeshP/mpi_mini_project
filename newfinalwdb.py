import cv2  # OpenCV library for computer vision tasks
import numpy as np  # NumPy for numerical operations
import mediapipe as mp  # MediaPipe for face detection
from cvzone.FaceDetectionModule import FaceDetector  # Face detection module from CVZone
from cvzone.SerialModule import SerialObject  # Serial communication module from CVZone
import sqlite3  # For SQLite database operations
from datetime import datetime  # To record the current date for attendance
import os  # To handle file paths

import time

# Initialize the webcam for video capture (default camera at index 0)
cap = cv2.VideoCapture(0)

# Create a FaceDetector object to detect faces in the video stream
detector = FaceDetector()

# Initialize the serial object to communicate with Arduino via the specified COM port
arduino = SerialObject('COM3')

# Connect to the SQLite database
conn = sqlite3.connect("database/finaldb.db")
cursor = conn.cursor()

# Function to load face encodings from the images stored in the database
def load_face_encodings():
    cursor.execute("SELECT student_id, image_path FROM students")
    students_data = cursor.fetchall()
    
    known_face_encodings = []
    known_student_ids = []
    
    for student_id, image_path in students_data:
        # print(student_id)
        # print(image_path)
        # Load the student's image from the stored path
        student_image = cv2.imread(image_path)
        
        # Convert the image to grayscale (or use another method if you prefer)
        student_image_gray = cv2.cvtColor(student_image, cv2.COLOR_BGR2GRAY)
        
        # Initialize the LBPH face recognizer
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        face_recognizer.train([student_image_gray], np.array([student_id]))
        
        # Append the recognizer and student_id to their respective lists
        known_face_encodings.append(face_recognizer)
        known_student_ids.append(student_id)
    
    return known_face_encodings, known_student_ids

# Function to check if the student is registered for the class
def is_student_registered(student_id, class_id):
    cursor.execute("SELECT * FROM registrations WHERE student_id = ? AND class_id = ?", (student_id, class_id))
    return cursor.fetchone() is not None

# # Function to mark attendance
# def mark_attendance(student_id, class_id):
#     # Get the current date
#     attendance_date = datetime.now().strftime("%Y-%m-%d")
    
#     # Check if attendance has already been marked for this student and class on the current date
#     cursor.execute("SELECT * FROM attendance WHERE student_id = ? AND class_id = ? AND attendance_date = ?",
#                    (student_id, class_id, attendance_date))
#     if cursor.fetchone() is None:
#         # If not already marked, insert the attendance record
#         cursor.execute("INSERT INTO attendance (student_id, class_id, attendance_date, is_present) VALUES (?, ?, ?, ?)",
#                        (student_id, class_id, attendance_date, 1))  # 1 means present
#         conn.commit()
#         print(f"Attendance marked for student {student_id} in class {class_id} on {attendance_date}")

# Dictionary to track the last time attendance was marked for each student in each class
attendance_cooldown = {}

# Cooldown time in seconds (e.g., 60 seconds to prevent re-marking attendance within 1 minute)
COOLDOWN_PERIOD = 60

# Function to mark attendance
def mark_attendance(student_id, class_id):
    current_time = time.time()
    attendance_date = datetime.now().strftime("%Y-%m-%d")

    # Check if attendance has already been marked for this student and class on the current date
    cursor.execute("SELECT * FROM attendance WHERE student_id = ? AND class_id = ? AND attendance_date = ?",
                   (student_id, class_id, attendance_date))
    
    if cursor.fetchone() is None:
        # Check the cooldown period
        key = (student_id, class_id)
        if key in attendance_cooldown:
            last_marked_time = attendance_cooldown[key]
            if current_time - last_marked_time < COOLDOWN_PERIOD:
                print(f"Attendance for student {student_id} in class {class_id} already marked recently. Skipping...")
                return  # Skip marking attendance if it's within the cooldown period

        # If not already marked and cooldown has passed, insert the attendance record
        cursor.execute("INSERT INTO attendance (student_id, class_id, attendance_date, is_present) VALUES (?, ?, ?, ?)",
                       (student_id, class_id, attendance_date, 1))  # 1 means present
        conn.commit()
        print(f"Attendance marked for student {student_id} in class {class_id} on {attendance_date}")

        # Update the cooldown timestamp for this student and class
        attendance_cooldown[key] = current_time
    else:
        print(f"Attendance already marked for student {student_id} in class {class_id} on {attendance_date}")


# Load the known face encodings from the database
known_face_encodings, known_student_ids = load_face_encodings()

last_detection_time = datetime.min
DETECTION_INTERVAL = 10
PRINT_INTERVAL = 5  # Set the print interval to 5 seconds
last_print_time = time.time()

# Start an infinite loop to continuously read frames from the webcam
while True:
    # Read a frame from the webcam (returns success flag and the frame)
    success, img = cap.read()

    # Convert the current frame from BGR to RGB for compatibility with MediaPipe's detection
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect faces in the current frame using the FaceDetector object
    img, dBoxes = detector.findFaces(img)

    current_time = datetime.now()
    if (current_time - last_detection_time).seconds >= DETECTION_INTERVAL:      
        # Check if at least one face is detected
        if dBoxes:
            # Extract the bounding box of the first detected face
            x, y, w, h = dBoxes[0]['bbox']

            # Crop the face region from the original RGB image using the bounding box coordinates
            face_region = img_rgb[y:y+h, x:x+w]

            # Convert the cropped face region to grayscale for recognition
            face_region_gray = cv2.cvtColor(face_region, cv2.COLOR_RGB2GRAY)

            # Iterate through the known face encodings to find a match
            for i, face_recognizer in enumerate(known_face_encodings):
                label, confidence = face_recognizer.predict(face_region_gray)
                threshold = 100  # Adjust the threshold for confidence

                if confidence < threshold:
                    student_id = known_student_ids[i]
                    class_id = 2  # Example class ID, you can map this dynamically
                    
                    # Check if the student is registered for the class
                    if is_student_registered(student_id, class_id):
                        # Mark attendance if the student is registered
                        mark_attendance(student_id, class_id)
                        arduino.sendData([0, 1])  # Send data to turn OFF the LED (face recognized)
                        if time.time() - last_print_time >= PRINT_INTERVAL:
                            print(f"Known face detected (Student ID: {student_id}). Attendance marked. LED OFF!")
                            last_print_time = time.time()  # Reset the last print time
                    else:
                        print(f"Student {student_id} not registered for class {class_id}.")
                    break
            else:
                arduino.sendData([1, 0])  # Send data to turn ON the LED (unknown face)
                print("Unknown face detected. LED ON.")
                last_print_time = time.time()
        else:
            # If no face is detected in the frame, turn ON the LED
            arduino.sendData([1, 0])
            print("No face detected. LED ON.")
            last_print_time = time.time()

    # Display the current frame with detected faces in a window
    cv2.imshow("Video", img)

    # Wait for the 'q' key to be pressed to break the loop and stop the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Close the SQLite connection when done
conn.close()
