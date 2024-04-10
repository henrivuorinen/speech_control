import cv2


class VideoStreamRecognition:
    def __init__(self):
        # Load the pre-trained model
        self.net = cv2.dnn.readNetFromCaffe("model/MobileNetSSD_deploy.prototxt",
                                            "model/MobileNetSSD_deploy.caffemodel")

        # List of class labels
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                        "sofa", "train", "tvmonitor", "phone", "human"]

        # Initialize the webcam
        self.camera = cv2.VideoCapture(0)  # Use the default webcam (index 0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def start(self):
        while True:
            ret, frame = self.camera.read()  # Read a frame from the webcam

            if not ret:
                break

            frame_resized = cv2.resize(frame, (300, 300))
            blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), 127.5)
            self.net.setInput(blob)
            detections = self.net.forward()

            # loop over detection
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]

                # filter out weak detections
                if confidence > 0.5:
                    class_id = int(detections[0, 0, i, 1])
                    label = self.CLASSES[class_id]

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

    def stop(self):
        self.camera.release()  # Release the webcam
        cv2.destroyAllWindows()
