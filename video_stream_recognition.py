import cv2
import numpy as np


class VideoStreamRecognition:
    def __init__(self):
        self.net = cv2.dnn.readNetFromCaffe("model/MobileNetSSD_deploy.prototxt",
                                            "model/MobileNetSSD_deploy.caffemodel")

        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                        "sofa", "train", "tvmonitor", "phone", "human"]

    def start(self, video_stream):
        while True:
            # Receive frame from the video stream
            frame = video_stream.read()

            # Perform object detection on the frame
            detections = self.detect_objects(frame)

            # Display the frame with detected objects
            self.display_frame(frame, detections)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def detect_objects(self, frame):
        frame_resized = cv2.resize(frame, (300, 300))
        blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()
        return detections

    def display_frame(self, frame, detections):
        # Process the detections and draw bounding boxes on the frame
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                class_id = int(detections[0, 0, i, 1])
                label = self.CLASSES[class_id]
                box = detections[0, 0, i, 3:7] * 300
                (startX, startY, endX, endY) = box.astype("int")
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
                cv2.putText(frame, label, (startX, startY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow("Object Detection", frame)

    def stop(self):
        cv2.destroyAllWindows()
