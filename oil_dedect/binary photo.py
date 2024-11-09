import numpy as np
import matplotlib.pyplot as plt
import cv2

def detect_oil_spill(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to detect the oil spill
    threshold = 0.5
    binary_image = gray_image > threshold

    # Differentiate between oil and water
    oil_pixels = binary_image.sum()
    water_pixels = image.size - oil_pixels

    # Calculate the percentage of oil pixels
    oil_percentage = oil_pixels / image.size * 100

    # Display the original image and the binary image in a new window
    cv2.imshow('Original Image', image)
    cv2.imshow('Binary Image', binary_image)

    # Display the percentage of oil pixels in a new window
    cv2.putText(image, f'Oil Percentage: {oil_percentage:.2f}%', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.imshow('Oil Percentage', image)

    # Wait for a key press to close the windows
    cv2.waitKey(0)

if __name__ == '__main__':
    # Get the image path from the user
    image_path = input("D:\project 2\oil_dedect\oil17.jpg")

    # Detect the oil spill
    detect_oil_spill(image_path)
