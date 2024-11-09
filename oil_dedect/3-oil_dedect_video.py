import cv2
import numpy as np

def detect_oil_in_video(video_path, target_frame_num):
    # Capture the video
    cap = cv2.VideoCapture(video_path)

    # Define the HSV range for oil
    oil_lower = np.array([0, 100, 100])
    oil_upper = np.array([25, 255, 255])

    oil_detected = False

    frame_count = 0
    while True:
        # Capture the current frame
        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        # Check if we've reached the target frame number
        if frame_count == target_frame_num:
            # Extract the target frame
            target_frame = frame.copy()

            # Convert the target frame to HSV color space
            target_hsv = cv2.cvtColor(target_frame, cv2.COLOR_BGR2HSV)

            # Create a mask for oil
            oil_mask = cv2.inRange(target_hsv, oil_lower, oil_upper)

            # Apply a morphological opening to the mask to remove noise
            oil_mask = cv2.morphologyEx(oil_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

            # Count the number of pixels in the mask
            oil_count = np.sum(oil_mask)

            # Check if oil was detected
            if oil_count > 1000:
                oil_detected = True
                break

    # Release the video capture
    cap.release()

    # Close all windows
    cv2.destroyAllWindows()

    return target_frame, oil_detected

# Example usage
video_path = "D:\project 2\oil_dedect\oilvideo0.mp4"
target_frame_num = 100  # Specify the target frame number
target_frame, oil_detected = detect_oil_in_video(video_path, target_frame_num)

if oil_detected:
   print(f"Oil detected in video  {video_path}")
else:
    print('No oil detected')
