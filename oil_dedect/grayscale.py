import cv2
import numpy as np

# Load the image
image = cv2.imread("D:\project 2\oil_dedect\oil17.jpg")

# Convert the image to grayscale
grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Create a histogram of the grayscale values
histogram = cv2.calcHist([grayscale_image], [0], None, [256], [0, 256])

# Count the number of pixels for each grayscale value
grayscale_values = np.arange(256)
grayscale_counts = histogram.ravel()

# Print the number of pixels for each grayscale value
for grayscale_value, grayscale_count in zip(grayscale_values, grayscale_counts):
    print(f"Grayscale value {grayscale_value}: {grayscale_count} pixels")
