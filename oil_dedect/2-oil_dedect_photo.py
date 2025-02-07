import cv2
import numpy as np
import os

photos_dir = "D:\project 2\oil_dedect\photos"

oil_detected_photos = [
"D:\project 2\oil_dedect\oil25.jpg",
"D:\project 2\oil_dedect\oil0.jpg",
"D:\project 2\oil_dedect\oil1.jpg",
"D:\project 2\oil_dedect\oil2.jpg",
"D:\project 2\oil_dedect\oil3.jpg",
"D:\project 2\oil_dedect\oil4.jpg",
"D:\project 2\oil_dedect\oil5.jpg",
"D:\project 2\oil_dedect\oil6.jpg",
"D:\project 2\oil_dedect\oil7.jpg",
"D:\project 2\oil_dedect\oil8.jpg",
"D:\project 2\oil_dedect\oil9.jpg",
"D:\project 2\oil_dedect\oil10.jpg",
"D:\project 2\oil_dedect\oil11.jpg",
"D:\project 2\oil_dedect\oil12.jpg",
"D:\project 2\oil_dedect\oil13.jpg",
"D:\project 2\oil_dedect\oil14.jpg",
"D:\project 2\oil_dedect\oil15.jpg",
"D:\project 2\oil_dedect\oil16.jpg",
"D:\project 2\oil_dedect\oil17.jpg",
"D:\project 2\oil_dedect\oil18.jpg",
"D:\project 2\oil_dedect\oil19.jpg",
"D:\project 2\oil_dedect\oil20.jpg",
"D:\project 2\oil_dedect\oil21.jpg",
"D:\project 2\oil_dedect\oil22.jpg",
"D:\project 2\oil_dedect\oil23.jpg",
"D:\project 2\oil_dedect\oil24.jpg"

]

def detect_oil(image_path):
    """Detects oil on the surface of water in an image.

    Args:
        image_path: The path to the image file.

    Returns:
        A boolean value indicating whether oil was detected in the image.
    """

    # Load the image.
    image = cv2.imread(image_path)

    # Convert the image to HSV color space.
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the HSV range for oil.
    oil_lower = np.array([0, 100, 100])
    oil_upper = np.array([25, 255, 255])

    # Create a mask for oil.
    oil_mask = cv2.inRange(hsv, oil_lower, oil_upper)

    # Apply a morphological opening to the mask to remove noise.
    oil_mask = cv2.morphologyEx(oil_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

    # Count the number of pixels in the mask.
    oil_count = np.sum(oil_mask)

    # Return True if the number of pixels in the mask is greater than a threshold.
    return oil_count > 1000

# Check for oil in each photo
for image_path in oil_detected_photos:
    oil_detected = detect_oil(image_path)

    if oil_detected:
        print(f"Oil detected in {image_path}")
    else:
        print(f"No oil detected in {image_path}")
