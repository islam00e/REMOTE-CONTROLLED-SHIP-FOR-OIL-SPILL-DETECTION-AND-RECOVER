import cv2
import numpy as np

def detect_oil_spills(video_capture):
    while True:
        ret, frame = video_capture.read()

        if not ret:
            break

        oil_spills = detect_oil_spills_on_frame(frame)

        if oil_spills:
            print("Oil spill detected!")

        for oil_spill in oil_spills:
            x, y, w, h = oil_spill
            cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 255, 0), 2)

        cv2.imshow('Oil Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def detect_oil_spills_on_frame(frame):
    # Enhance contrast using Adaptive Histogram Equalization (AHE)
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    equalized_image = clahe.apply(gray_image)

    # Apply Otsu's thresholding to segment oil regions
    _, thresholded_image = cv2.threshold(equalized_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Apply color filter to identify oil spills
    oil_spill_mask = cv2.inRange(frame, (0, 100, 100), (25, 225, 225))

    # Refine oil regions using morphological operations
    kernel = np.ones((3, 3), np.uint8)
    eroded_image = cv2.erode(oil_spill_mask, kernel, iterations=2)
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

    # Apply additional filtering based on oil spill characteristics
    filtered_oil_spills = []
    for oil_spill in oil_spills:
        x, y, w, h = oil_spill

        # Water Reflection Filtering
        avg_intensity = np.mean(frame[y:y + h, x:x + w])
        if avg_intensity > 150:
            continue

        # Edge Detection
        edges = cv2.Canny(frame, 50, 150)
        edge_count = np.sum(edges[y:y + h, x:x + w])
        if edge_count < 100:
            continue

        # Texture Analysis
        variance = np.var(frame[y:y + h, x:x + w])
        if variance < 200:
            continue

        filtered_oil_spills.append(oil_spill)

    return filtered_oil_spills

# Create a VideoCapture object to capture frames from the webcam
video_capture = cv2.VideoCapture(0)

# Detect oil spills from live camera video
detect_oil_spills(video_capture)
