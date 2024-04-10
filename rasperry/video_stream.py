import io
import picamera
import socket
import struct
import time
import threading

# Function to handle video stream
def video_stream():
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
            while True:
                camera.wait_recording(1)
    finally:
        connection.close()
        server_socket.close()

video_thread = threading.Thread(target=video_stream)
video_thread.start()