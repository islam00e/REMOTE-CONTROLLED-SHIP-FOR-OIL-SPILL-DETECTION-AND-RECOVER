import os
import cv2

# Define data directory and class names
data_dir = "oil_spill_dataset"
class_names = ["oil_spill"]

# Create directories for training, validation, and testing sets
os.makedirs(os.path.join(data_dir, "train"), exist_ok=True)
os.makedirs(os.path.join(data_dir, "valid"), exist_ok=True)
os.makedirs(os.path.join(data_dir, "test"), exist_ok=True)

# Split images into training, validation, and testing sets
training_images, validation_images, testing_images = [], [], []

# Annotate images with bounding boxes
for image_path in os.listdir(data_dir):
    if image_path.endswith(".jpg") or image_path.endswith(".png"):
        image = cv2.imread(os.path.join(data_dir, image_path))
        # Manually annotate the image with bounding boxes
        # Save the annotated image and its corresponding label file
