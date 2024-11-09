import cv2
import numpy as np

def analyze_image(image_path):
    try:
        # Read the image
        image = cv2.imread(image_path)

        # Check if the image was loaded successfully
        if image is None:
            raise Exception("Failed to load image")

        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply edge detection to the grayscale image
        edges = cv2.Canny(gray_image, 50, 150)

        # Display the original image and the edges image in new windows
        cv2.imshow('Original Image', image)
        cv2.imshow('Edges Image', edges)

        # Wait for a key press to close the windows
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except Exception as e:
        print("Error:", e)

# Get the image path from the user
image_path = input("oil6.jpg ")

# Analyze the image and display the results
analyze_image(image_path)
