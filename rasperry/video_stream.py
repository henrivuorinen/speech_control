import cv2
import socket
import struct
import threading
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VideoStream")

# Flag to control video streaming
video_streaming = False
video_thread = None

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
    global video_streaming, video_thread
    if video_streaming:
        video_streaming = False
        if video_thread:
            video_thread.join()
            video_thread = None
        logger.info("Video stream stopped.")
    else:
        logger.warning("Video stream is not running.")

def video_stream():
    global video_streaming
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
        libcamera_process = subprocess.Popen(libcamera_command, stdout=subprocess.PIPE)

        try:
            while video_streaming:
                # Read frame from libcamera-hello subprocess
                frame_bytes = libcamera_process.stdout.read(640 * 480 * 3)

                if not frame_bytes:
                    break

                # Send frame size and frame data over the connection
                connection.sendall(struct.pack('<L', len(frame_bytes)))
                connection.sendall(frame_bytes)
        except Exception as e:
            logger.error(f"An error occurred during video streaming: {e}")
        finally:
            # Terminate libcamera-hello subprocess
            libcamera_process.terminate()
            libcamera_process.wait()
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
