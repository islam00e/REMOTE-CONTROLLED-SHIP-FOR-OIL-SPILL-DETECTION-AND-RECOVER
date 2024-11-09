import cv2
import numpy as np

def extract_color_features(image_path):
    # Load the image using the provided path
    image = cv2.imread(image_path)

    # Convert the image to BGR color space
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Calculate mean RGB values
    mean_rgb = np.mean(image_bgr, axis=(0, 1))

    # Extract saturation component from HSV color space
    image_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    saturation = image_hsv[:, :, 1]

    # Compute color difference between each pixel and reference clean water color
    reference_color = np.array([255, 255, 255])
    color_diff = np.linalg.norm(image_bgr - reference_color, axis=2)

    return mean_rgb, saturation, color_diff

# Extract color features for the image at "D:\project 2\oil_dedect\oil1.jpg"
mean_rgb, saturation, color_diff = extract_color_features("D:\project 2\oil_dedect\oil1.jpg")

print("Mean RGB values:", mean_rgb)
print("Saturation:", saturation)
print("Color difference:", color_diff)
