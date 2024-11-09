import cv2
import numpy as np
import serial

# Open a serial connection to Arduino
ser = serial.Serial('COM3', 9600)  # Adjust 'COM3' to the correct port and 9600 to the correct baud rate

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    # Convert frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define range of oil in HSV
    lower_oil = np.array([0, 100, 100])
    upper_oil = np.array([25, 255, 255])
    
    # Threshold the HSV image to get only oil
    mask = cv2.inRange(hsv_frame, lower_oil, upper_oil)
    
    # Apply a Gaussian blur to the mask to reduce noise
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    
    # Find contours of oil objects in the mask
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw contours around oil objects in the original frame
    total_oil_area = 0
    oil_detected = False
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:  # adjust this threshold as necessary
            cv2.drawContours(frame, [contour], 0, (0, 255, 255), 2)
            total_oil_area += area
            oil_detected = True
    
    # Print and send messages based on oil detection status
    if oil_detected:
        print("Oil detected")
        # Send the oil detection message to Arduino
        ser.write("oil detected\n".encode())
        
        # Print the total area of detected oil regions
        print("Total Oil Area:", total_oil_area)        
        # Send the total area to Arduino
        ser.write(f"total oil area: {total_oil_area}\n".encode())
    else:
        print("No oil detected")
        # Send the no oil detection message to Arduino
        ser.write("no oil detected\n".encode())

    # Display the resulting frame
    cv2.imshow('oil detect', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
