import logging
from time import sleep
import threading
from autonomous_movement import start_obstacle_avoidance, stop_autonomous_movement
from motor_control import move_forward, move_backward, turn_left, turn_right, stop_motors
from video_stream import start_video_stream, stop_video_stream

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

autonomous_thread = None  # Global variable to hold the autonomous movement thread

def execute_command(command):
    global autonomous_thread  # Declare autonomous_thread as global
    if command == "move forward":
        move_forward(0.7)
        logger.info("Moving forward")
    elif command == "move backwards":
        move_backward(0.7)
        logger.info("Moving backwards")
    elif command == "turn left":
        turn_left(0.7)
        logger.info("Turning left")
        sleep(0.4)
        stop_motors()
    elif command == "turn right":
        turn_right(0.7)
        logger.info("Turning right")
        sleep(0.4)
        stop_motors()
    elif command == "set free":
        if not autonomous_thread or not autonomous_thread.is_alive():
            autonomous_thread = threading.Thread(target=start_obstacle_avoidance)
            autonomous_thread.start()
        logger.info("Autonomous movement started")
    elif command == "stop moving":
        stop_autonomous_movement()
        logger.info("Stopping movement")
    elif command == "dance":
        turn_left(0.7)
        logger.info("Dancing")
        sleep(5)
        stop_motors()
        turn_right(0.7)
        sleep(5)
        stop_motors()
    elif command == "start video":
        start_video_stream()
        logger.info("Starting video stream")
    elif command == "stop video":
        stop_video_stream()
        logger.info("Stopping video stream")
    elif command == "stop":
        stop_motors()
        logger.info("Stopping")
    elif command == ("shut down"):
        logger.info("Shutting down")
        stop_motors()
    else:
        logger.warning(f"Unknown command: {command}")
        stop_motors()
