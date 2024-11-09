import cv2
import numpy as np
printed = False

# Specify the device ID of the external webcam
cap = cv2.VideoCapture(0)  # Replace 1 with the actual device ID

while True:
    ret, frame = cap.read()

    # Convert frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of oil detection in HSV
    lower_yellow = np.array([20, 70, 100])
    upper_yellow = np.array([40, 140, 225])

    # Threshold the HSV image to get only yellow colors
    mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)

    # Apply a Gaussian blur to the mask to reduce noise
    mask = cv2.GaussianBlur(mask, (5, 5), 0)

    # Find contours of yellow objects in the mask
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours around yellow objects in the original frame
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:  # adjust this threshold as necessary
            cv2.drawContours(frame, [contour], 0, (0, 255, 255), 2)
            print("oil is detected")
            printed = True

    # Display the resulting frame
    cv2.imshow('oil detect', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
