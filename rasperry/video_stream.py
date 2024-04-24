import cv2
import socket
import struct
import threading
import subprocess

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

            # Send frame size and frame data over the connection
            connection.sendall(struct.pack('<L', len(frame_bytes)))
            connection.sendall(frame_bytes)

    finally:
        # Terminate libcamera-hello subprocess
        libcamera_process.terminate()

        # Release resources
        server_socket.close()

# Test the video streaming functionality
if __name__ == "__main__":
    start_video_stream()
