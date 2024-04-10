import io
import picamera
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
        # create connection to the camera module
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.framerate = 24
            camera.start_recording(connection, format='h264')
            while video_streaming:
                camera.wait_recording(1)
    finally:
        connection.close()
        server_socket.close()
