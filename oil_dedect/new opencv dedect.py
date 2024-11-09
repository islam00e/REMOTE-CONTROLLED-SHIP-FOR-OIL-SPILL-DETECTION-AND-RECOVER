import cv2
import numpy as np

def detect_oil_spills(video_capture):
    while True:
        # Capture the current frame
        ret, frame = video_capture.read()

        if not ret:
            break

        # Convert to HSV color space
        hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define lower and upper bounds for oil color in HSV
        lower_oil_hue = 10
        upper_oil_hue = 30
        lower_oil_saturation = 50
        upper_oil_saturation = 100
        lower_oil_value = 50
        upper_oil_value = 100

        # Create a mask for oil regions based on color
        oil_mask = cv2.inRange(hsv_image,
                               (lower_oil_hue, lower_oil_saturation, lower_oil_value),
                               (upper_oil_hue, upper_oil_saturation, upper_oil_value))

        # Apply morphological operations to refine oil regions
        kernel = np.ones((5, 5), np.uint8)
        opened_oil_mask = cv2.morphologyEx(oil_mask, cv2.MORPH_OPEN, kernel, iterations=2)
        closed_oil_mask = cv2.morphologyEx(opened_oil_mask, cv2.MORPH_CLOSE, kernel, iterations=2)

        # Identify connected components as potential oil spills
        contours, _ = cv2.findContours(closed_oil_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Analyze contours to filter out noise and generate bounding boxes
        oil_spills = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:  # Filter out small contours (noise)
                x, y, w, h = cv2.boundingRect(contour)
                oil_spills.append((x, y, w, h))

        # Refine oil spill detection using edge detection and texture analysis
        refined_oil_spills = []
        for oil_spill in oil_spills:
            x, y, w, h = oil_spill

            # Extract the oil spill region
            oil_spill_region = frame[y:y + h, x:x + w]

            # Convert to grayscale for edge detection
            grayscale_oil_spill = cv2.cvtColor(oil_spill_region, cv2.COLOR_BGR2GRAY)

            # Apply Canny edge detection
            edges = cv2.Canny(grayscale_oil_spill, 50, 150)

            # Calculate edge density
            edge_density = np.mean(edges)

            # Analyze texture using Gabor filters
            gabor_filters = cv2.getGaborKernel((31, 31), 8, np.pi / 4, 16, 0.5, 0.3)
            filtered_oil_spill = cv2.filter2D(grayscale_oil_spill, -1, gabor_filters)
            texture_mean = np.mean(filtered_oil_spill)

            # Combine edge density and texture mean to determine confidence score
            confidence_score = edge_density * texture_mean

            # Add refined oil spill with confidence score to the list
            if confidence_score > 0.5:
                refined_oil_spills.append((oil_spill, confidence_score))

        # Draw bounding boxes around detected oil spills
        for oil_spill in refined_oil_spills:
            x, y, w, h, confidence_score = oil_spill

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0,
                             255, 0), 2)

            # Display the confidence score next to the bounding box
            cv2.putText(frame, str(confidence_score), (x + w, y + h),
                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        # Display the frame
