import cv2
import numpy as np

def detect_oil(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Otsu's thresholding to segment the oil from the water
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Find the contours of the oil blobs
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if there are any oil blobs detected
    if len(contours) > 0:
        return True
    else:
        return False

# Load the image of the water surface
image = cv2.imread('oil_spill.jpg')

# Detect oil on the water surface
is_oil_detected = detect_oil(image)

# Print the result
if is_oil_detected:
    print('Oil detected in the photo!')
else:
    print('No oil detected in the photo.')
