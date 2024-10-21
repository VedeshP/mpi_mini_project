import mediapipe as mp
import cv2
from cvzone.FaceDetectionModule import FaceDetector
from cvzone.SerialModule import SerialObject

cap = cv2.VideoCapture(0)
detector = FaceDetector()
arduino = SerialObject('COM3')

while True:
    success, img = cap.read()
    img, dBoxes = detector.findFaces(img)

    if dBoxes:
        arduino.sendData([0, 1])
    else:
        arduino.sendData([1, 0])

    cv2.imshow("Video", img)
    cv2.waitKey(1)