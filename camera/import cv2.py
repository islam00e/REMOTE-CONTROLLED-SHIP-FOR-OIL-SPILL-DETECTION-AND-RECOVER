import cv2

# Capture video from webcam
cap = cv2.VideoCapture(0)

while True:
    # Read the next frame
    ret, frame = cap.read()

    # Display the frame
    cv2.imshow('Webcam Live Feed', frame)

    # Check if the user wants to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the webcam
cap.release()
cv2.destroyAllWindows()
