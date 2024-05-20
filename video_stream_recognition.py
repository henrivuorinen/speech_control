import cv2
import numpy as np
import socket
import struct
import threading

class VideoStreamRecognition:
    def __init__(self):
        self.net = cv2.dnn.readNetFromCaffe("model/MobileNetSSD_deploy.prototxt",
                                            "model/MobileNetSSD_deploy.caffemodel")
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                        "sofa", "train", "tvmonitor", "phone", "human"]

        self.server_ip = "10.42.0.1"  # Replace with the Raspberry Pi's IP address
        self.server_port = 8000
        self.client_socket = None
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._stream_video)
            self.thread.start()

    def _stream_video(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Add a print statement to verify the server IP and port
        print(f"Attempting to connect to server at {self.server_ip}:{self.server_port}")
        self.client_socket.connect((self.server_ip, self.server_port))
        # Add a print statement to indicate successful connection
        print("Connection to server established")

        try:
            while self.running:
                # Receive frame size
                frame_size_bytes = self.client_socket.recv(4)
                if not frame_size_bytes:
                    break
                frame_size = struct.unpack('<L', frame_size_bytes)[0]

                # Receive frame data
                frame_data = b''
                while len(frame_data) < frame_size:
                    chunk = self.client_socket.recv(frame_size - len(frame_data))
                    if not chunk:
                        raise RuntimeError("Incomplete frame data received")
                    frame_data += chunk

                # Convert frame data to numpy array
                frame_nparr = np.frombuffer(frame_data, np.uint8)
                frame = cv2.imdecode(frame_nparr, cv2.IMREAD_COLOR)

                # Display the frame using OpenCV
                cv2.imshow("Video Feed", frame)
                cv2.waitKey(1)  # Wait for a short duration to display the frame

                # Perform object detection on the frame
                detections = self.detect_objects(frame)

                # Display the frame with detected objects
                self.display_frame(frame, detections)

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            self.client_socket.close()

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
        if self.running:
            self.running = False
            if self.thread is not None:
                self.thread.join()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    video_stream_recognition = VideoStreamRecognition()
    video_stream_recognition.start()
