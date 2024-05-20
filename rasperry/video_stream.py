import cv2
import socket
import struct
import threading
import subprocess
import logging
import signal
import os

import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VideoStream")

# Flag to control video streaming
video_streaming = False
video_thread = None
libcamera_process = None

def start_video_stream():
    global video_streaming, video_thread
    if not video_streaming:
        video_streaming = True
        video_thread = threading.Thread(target=video_stream)
        video_thread.start()
        logger.info("Video stream started.")
    else:
        logger.warning("Video stream is already running.")

def stop_video_stream():
    global video_streaming, video_thread, libcamera_process
    if video_streaming:
        video_streaming = False
        if video_thread:
            video_thread.join()
            video_thread = None
        if libcamera_process:
            libcamera_process.terminate()
            libcamera_process.wait()
            libcamera_process = None
        logger.info("Video stream stopped.")
    else:
        logger.warning("Video stream is not running.")

def video_stream():
    global video_streaming, libcamera_process
    # Create TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Bind the socket to the address and port
        server_socket.bind(('0.0.0.0', 8000))
        server_socket.listen(1)
        logger.info("Waiting for a connection...")

        connection, client_address = server_socket.accept()
        logger.info(f"Connection from {client_address}")

        # Start libcamera-hello subprocess
        libcamera_command = ["libcamera-hello", "--camera", "0", "-t", "0"]
        libcamera_process = subprocess.Popen(libcamera_command, stdout=subprocess.PIPE, preexec_fn=os.setsid)

        try:
            while video_streaming:
                # Read frame from libcamera-hello subprocess
                frame_bytes = libcamera_process.stdout.read(640 * 480 * 3)

                if not frame_bytes:
                    break

                # Rotate the frame data by 180 degrees
                frame = np.frombuffer(frame_bytes, dtype=np.uint8).reshape(480, 640, 3)  # Assuming frame dimensions are 640x480
                rotated_frame = cv2.rotate(frame, cv2.ROTATE_180)

                # Convert the rotated frame back to bytes
                rotated_frame_bytes = rotated_frame.tobytes()

                # Send rotated frame size and frame data over the connection
                connection.sendall(struct.pack('<L', len(rotated_frame_bytes)))
                connection.sendall(rotated_frame_bytes)
        except Exception as e:
            logger.error(f"An error occurred during video streaming: {e}")
        finally:
            # Terminate libcamera-hello subprocess
            if libcamera_process:
                os.killpg(os.getpgid(libcamera_process.pid), signal.SIGTERM)
                libcamera_process.wait()
                libcamera_process = None
            connection.close()
            logger.info("Connection closed.")
    except Exception as e:
        logger.error(f"An error occurred while setting up the server: {e}")
    finally:
        server_socket.close()
        logger.info("Server socket closed.")

# Test the video streaming functionality
if __name__ == "__main__":
    start_video_stream()
