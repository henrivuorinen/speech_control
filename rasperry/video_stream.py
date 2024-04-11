import cv2
import socket
import struct
import time
import threading

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
    connection = server_socket.accept()[0].makefile("wb")

    try:
        # Initialize OpenCV capture
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        while video_streaming:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to bytes and send it over the connection
            frame = cv2.imencode('.jpg', frame)[1].tostring()
            connection.write(struct.pack('<L', len(frame)))
            connection.write(frame)

    finally:
        connection.close()
        server_socket.close()
