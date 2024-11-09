import darknet

# Download pre-trained YOLOv5 weights
darknet.download_pretrained("yolov5s.pt")

# Prepare configuration file
config_file = "yolov5s.cfg"
meta_file = "coco.data"

# Train YOLO model
darknet.train(config_file, meta_file, darknet.load_model("yolov5s.pt"))
