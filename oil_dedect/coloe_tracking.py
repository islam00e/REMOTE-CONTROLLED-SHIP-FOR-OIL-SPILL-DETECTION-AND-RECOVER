import cv2
import sys
import numpy as np

def nothing(x):
    pass

def track_color(image_path=None):
    use_camera = False

    # Check if filename is passed
    if len(sys.argv) <= 1:
        print("'Usage: python hsvThresholder.py <ImageFilePath>' to ignore camera and use a local image.")
        use_camera = True

    # Create a window
    cv2.namedWindow('image')

    # Define trackbar callback function
    def trackbar_callback(x):
        # Update min and max HSV values based on trackbar positions
        h_min = cv2.getTrackbarPos('HMin', 'image')
        s_min = cv2.getTrackbarPos('SMin', 'image')
        v_min = cv2.getTrackbarPos('VMin', 'image')

        h_max = cv2.getTrackbarPos('HMax', 'image')
        s_max = cv2.getTrackbarPos('SMax', 'image')
        v_max = cv2.getTrackbarPos('VMax', 'image')

        # Set minimum and max HSV values to display
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])

        # Create HSV Image and threshold into a range.
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(img, img, mask=mask)

        # Display output image
        cv2.imshow('image', output)

    # Create trackbars for color change
    cv2.createTrackbar('HMin', 'image', 0, 179, trackbar_callback)
    cv2.createTrackbar('SMin', 'image', 0, 255, trackbar_callback)
    cv2.createTrackbar('VMin', 'image', 0, 255, trackbar_callback)
    cv2.createTrackbar('HMax', 'image', 0, 179, trackbar_callback)
    cv2.createTrackbar('SMax', 'image', 0, 255, trackbar_callback)
    cv2.createTrackbar('VMax', 'image', 0, 255, trackbar_callback)

    # Set default value for MAX HSV trackbars.
    cv2.setTrackbarPos('HMax', 'image', 179)
    cv2.setTrackbarPos('SMax', 'image', 255)
    cv2.setTrackbarPos('VMax', 'image', 255)

    # Output Image to display
    if use_camera:
        cap = cv2.VideoCapture(0)
        # Wait longer to prevent freeze for videos.
        wait_time = 330
    else:
        # Read image from file
        img = cv2.imread("D:\project 2\oil_dedect\oil19.jpg")
        output = img
        wait_time = 33

    while (True):
        if use_camera:
            # Capture frame-by-frame
            ret, img = cap.read()
            if not ret:
                break
            output = img

        # Track and isolate specific colors
        trackbar_callback(0)

        # Wait for key press
        if cv2.waitKey(wait_time) & 0xFF == ord('q'):
            break

    # Release resources
    if use_camera:
        cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        track_color(image_path)
    else:
        track_color()
