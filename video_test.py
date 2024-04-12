import tensorflow as tf
import numpy as np
import sys
import os
import cv2
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

net = cv2.dnn.readNetFromCaffe("model/MobileNetSSD_deploy.prototxt", "model/MobileNetSSD_deploy.caffemodel")

# List of class labels
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

cap = cv2.VideoCapture(0)

while True:
    # Read from webcam
    ret, frame = cap.read()

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

    # Break the loop if q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()