import cv2
import numpy as np

def detect_oil_spills(video_capture):
    while True:
        # Capture the current frame
        ret, frame = video_capture.read()

        if not ret:
            break

        # Detect oil spills in the current frame
        oil_spills = detect_oil_spills_on_frame(frame)

        # Draw bounding boxes around detected oil spills
        for oil_spill in oil_spills:
            x, y, w, h = oil_spill
            cv2.rectangle(frame, (x, y), (x+w, y+h), (100, 255, 0), 2)

        # Display the frame with detected oil spills
        cv2.imshow('Oil Detection', frame)

        # Check for 'q' key to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def detect_oil_spills_on_frame(frame):
    # Convert frame to grayscale
    grayscale_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply histogram equalization to enhance contrast
    equalized_image = cv2.equalizeHist(grayscale_image)

    # Apply Otsu's thresholding to segment oil regions
    _, thresholded_image = cv2.threshold(equalized_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Apply morphological operations to refine oil regions
    kernel = np.ones((3, 3), np.uint8)
    eroded_image = cv2.erode(thresholded_image, kernel, iterations=2)
    dilated_image = cv2.dilate(eroded_image, kernel, iterations=2)

    # Identify connected components as oil spills
    contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Analyze contours to filter out noise and generate bounding boxes
    oil_spills = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:  # Filter out small contours (noise)
            x, y, w, h = cv2.boundingRect(contour)
            oil_spills.append((x, y, w, h))

    # Return detected oil spills
    return oil_spills

# Create a VideoCapture object to capture frames from the camera
video_capture = cv2.VideoCapture(0)

# Detect oil spills from live camera video
detect_oil_spills(video_capture)
