import cv2
import numpy as np
printed = False
cap = cv2.VideoCapture(0)

while True:
  # Delay for 5 seconds
  cv2.waitKey(500)

  # Capture the next frame
  ret, frame = cap.read()

  # Check if frame is read successfully
  if not ret:
    break

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
  for contour in contours:
    area = cv2.contourArea(contour)
    if area > 100: # adjust this threshold as necessary
      cv2.drawContours(frame, [contour], 0, (0, 255, 255), 2)
      print(f"Oil detected! Area: {area}")
      printed = True

  # Display the resulting frame
  cv2.imshow('oil detect', frame)

  # Press 'q' to quit
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# Release capture and destroy windows
cap.release()
cv2.destroyAllWindows()
