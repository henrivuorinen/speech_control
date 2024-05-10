import cv2
import socket
import struct
import threading
import subprocess
import numpy as np

# Load the pre-trained MobileNet SSD model
net = cv2.dnn.readNetFromCaffe("model/MobileNetSSD_deploy.prototxt", "model/MobileNetSSD_deploy.caffemodel")

# List of class labels
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

# Flag to control video streaming
video_streaming = False

# Function to start video streaming
def start_video_stream():
    global video_streaming
    video_streaming = True
    video_thread = threading.Thread(target=video_stream)
    video_thread.start()

# Function to stop video streaming
def stop_video_stream():
    global video_streaming
    video_streaming = False

# Function to handle video stream
def video_stream():
    global video_streaming
    # Create TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the address and port
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)

    # Accept a single connection
    connection = server_socket.accept()[0]

    # Start libcamera-hello subprocess
    libcamera_command = ["libcamera-hello", "--camera", "0", "-t", "0"]
    libcamera_process = subprocess.Popen(libcamera_command, stdout=subprocess.PIPE)

    try:
        while video_streaming:
            # Read frame from libcamera-hello subprocess
            frame_bytes = libcamera_process.stdout.read(640*480*3)

            # Decode frame bytes to numpy array
            frame = cv2.imdecode(np.frombuffer(frame_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)

            # Resize the frame and preprocess for object detection
            frame_resized = cv2.resize(frame, (300, 300))
            blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), 127.5)
            net.setInput(blob)
            detections = net.forward()

            # Log the relevant information about detected objects
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]

                # Filter out weak detections
                if confidence > 0.5:
                    class_id = int(detections[0, 0, i, 1])
                    label = CLASSES[class_id]

                    # Extract coordinates of the bounding box
                    box = detections[0, 0, i, 3:7] * 300
                    (startX, startY, endX, endY) = box.astype("int")

                    # Log the detected object and its confidence score
                    print(f"Detected {label} with confidence score: {confidence}")

                    # Draw box around the detected object
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
                    cv2.putText(frame, label, (startX, startY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Display the output frame
            cv2.imshow("Object Detection", frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Terminate libcamera-hello subprocess
        libcamera_process.terminate()

        # Release resources
        server_socket.close()

# Test the video streaming functionality
if __name__ == "__main__":
    start_video_stream()
