import cv2
import numpy as np

# Define oil detection parameters
lower_oil = np.array([0, 100, 100])
upper_oil = np.array([25, 255, 255])
min_area = 100  # Minimum area for oil detection

# Initialize variables
largest_area = 0
largest_contour = None
largest_side = None

# Capture video
cap = cv2.VideoCapture(0)

prev_frame = None  # Store previous frame for optical flow calculation

while True:
    # Read frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Calculate optical flow
    if prev_frame is not None:
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flow, _ = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        # Calculate average camera motion
        avg_motion = np.mean(flow, axis=0)

        # Adjust displayed frame
        shifted_frame = cv2.warpAffine(frame, np.array([[1, 0, -avg_motion[0]], [0, 1, -avg_motion[1]]]), dsize=frame.shape[:2])

        # Process shifted frame for oil detection
        mask = cv2.inRange(cv2.cvtColor(shifted_frame, cv2.COLOR_BGR2HSV), lower_oil, upper_oil)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Identify largest oil object
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > min_area and area > largest_area:
                largest_area = area
                largest_contour = contour

        # Determine largest side
        if largest_contour is not None:
            # Get bounding box
            x, y, w, h = cv2.boundingRect(largest_contour)

            # Check side with larger dimension
            if w > h:
                largest_side = "right"
            else:
                largest_side = "left"

            # Print information
            print(f"Largest oil detected on the {largest_side}")
            print(f"Area: {largest_area}")

            # Draw contour on shifted frame
            cv2.drawContours(shifted_frame, [largest_contour], 0, (0, 255, 255), 2)

        # Display frame
        cv2.imshow('oil detect', shifted_frame)

    # Update previous frame
    prev_frame = frame

    # Wait for key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
