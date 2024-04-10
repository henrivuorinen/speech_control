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
"""
MODEL_PATH = "../../sähköpaja/model"
LABEL_MAP_PATH = '../../labels_map'

#Load the model
model = tf.saved_model.load(MODEL_PATH)

#Load the label map
category_index = label_map_util.create_category_index_from_labelmap(LABEL_MAP_PATH, use_display_name=True)

#Replace with the IP address to correct ESP32 address
url = "http/localhostid/stream"

cap = cv2.VideoCapture(url)

while True:
    #Read a frame from the video stream
    ret, frame = cap.read()

    input_tensor = tf.convert_to_tensor([frame])
    detections = model(input_tensor)

    # visualize the results on the frame
    vis_util.visualize_boxes_and_labels_on_image_array(
        frame,
        np.squeeze(detections['detection_boxes']),
        np.squeeze(detections['detection_classes']).astype(np.int32),
        np.squeeze(detections['detection_scores']),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8
    )

    # display the frame with object detection results
    cv2.imshow('Object Detection', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
"""
