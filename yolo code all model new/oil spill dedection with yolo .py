import darknet
import cv2

# Load trained YOLO model
model = darknet.load_model("D:\yolo code all model new")
meta = darknet.load_meta("coco.data")

# Detect oil spills in video
cap = cv2.VideoCapture("video.mp4")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB format
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Resize the frame to the input size of the YOLO model
    frame = cv2.resize(frame, (608, 608))

    # Convert the frame to a NumPy array
    frame = np.asarray(frame)

    # Convert the frame to a list of blobs
    blobs = darknet.to_blob(frame, 3)

    # Run the YOLO object detection on the frame
    detections = darknet.network_predict(model, blobs)

    # Process the detections
    for detection in detections:
        confidence = detection[2]
        x, y, w, h = detection[3:7]
        label = meta[int(detection[0])]

        if label == "oil_spill":
            # Draw a bounding box around the detected oil spill
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Draw a label on top of the bounding box
            cv2.putText(
                frame,
                f"Oil spill: {confidence:.2f}",
                (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

    # Display the frame with the detected oil spills
    cv2.imshow("Oil Spill Detection", frame)

    # Check if the user wants to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Close the video capture source
