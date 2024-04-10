import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import sys
import os
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# Load the pre-trained model
net = cv2.dnn.readNetFromCaffe("model/MobileNetSSD_deploy.prototxt", "model/MobileNetSSD_deploy.caffemodel")

# List of class labels
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor", "phone", "human"]

# Initialize the PiCamera
camera = PiCamera()
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera)

# Allow the camera to warmup
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Convert the frame to an array
    frame = frame.array

    frame_resized = cv2.resize(frame, (300, 300))
    blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    # loop over detection
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # filter out weak detections
        if confidence > 0.5:
            class_id = int(detections[0, 0, i, 1])
            label = CLASSES[class_id]

            # Draw box around the detected object
            box = detections[0, 0, i, 3:7] * 300
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
            cv2.putText(frame, label, (startX, startY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # display the output frame
    cv2.imshow("Object Detection", frame)

    # Clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # Break the loop if q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close any open windows
camera.close()
cv2.destroyAllWindows()
