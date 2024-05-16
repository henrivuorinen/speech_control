import os
import subprocess
import threading
import logging
import signal
import cv2
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
        video_thread = threading.Thread(target=run_video_stream)
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

def run_video_stream():
    global video_streaming, libcamera_process
    libcamera_command = ["libcamera-hello", "--camera", "0", "-t", "0", "--output", "-"]
    libcamera_process = subprocess.Popen(libcamera_command, stdout=subprocess.PIPE, preexec_fn=os.setsid)
    try:
        while video_streaming:
            frame_bytes = libcamera_process.stdout.read(640 * 480 * 3)
            if not frame_bytes:
                break
            frame = np.frombuffer(frame_bytes, dtype=np.uint8).reshape((480, 640, 3))
            ret, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
    except Exception as e:
        logger.error(f"An error occurred during video streaming: {e}")
    finally:
        if libcamera_process:
            os.killpg(os.getpgid(libcamera_process.pid), signal.SIGTERM)
            libcamera_process.wait()
            libcamera_process = None
        logger.info("Video stream process terminated.")
