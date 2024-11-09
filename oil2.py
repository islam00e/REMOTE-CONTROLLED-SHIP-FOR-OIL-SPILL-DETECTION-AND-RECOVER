from ultralytics import YOLO
import cv2
import math
import serial
import time

# Running real-time from webcam
cap = cv2.VideoCapture(0)
model = YOLO('best.pt')

# Reading the classes
classnames = ['oil']

# Initialize serial communication with Arduino
arduino = serial.Serial('COM6', 9600)  # Adjust 'COM6' with the correct port

pump_running = False  # Variable to track pump status

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    result = model(frame, stream=True)

    # Flag to check if oil is detected
    oil_detected = False

    # Getting bbox, confidence, and class names information to work with
    for info in result:
        boxes = info.boxes
        for box in boxes:
            confidence = box.conf[0]
            confidence = math.ceil(confidence * 100)
            Class = int(box.cls[0])
            if confidence > 50 and classnames[Class] == 'oil':
                oil_detected = True
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
                cv2.putText(frame, f'{classnames[Class]} {confidence}%', [x1 + 8, y1 + 100],
                            scale=1.5, thickness=2)

    # Send signal to Arduino based on oil detection
    if oil_detected and not pump_running:
        print("Oil detected, starting pump")
        arduino.write(b"oil detected\n")  # Send 'oil detected' to Arduino
        pump_running = True

    elif not oil_detected and pump_running:
        print("No oil detected, stopping pump")
        arduino.write(b"no oil detected\n")  # Send 'no oil detected' to Arduino
        pump_running = False
        time.sleep(2)  # Add a delay before starting the valve
        arduino.write(b"start valve\n")  # Send 'start valve' to Arduino

    cv2.imshow('frame', frame)
    cv2.waitKey(1)
    time.sleep(1)  # Add a delay to avoid flooding the serial port
