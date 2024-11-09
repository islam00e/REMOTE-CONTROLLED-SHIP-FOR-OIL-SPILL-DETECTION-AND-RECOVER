import cv2
import numpy as np

# Load the image
image = cv2.imread('human.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply a threshold to the image to segment the human
thresh, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Find the contours of the human
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw a bounding box around the human
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Display the image
cv2.imshow('Detected Human', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
