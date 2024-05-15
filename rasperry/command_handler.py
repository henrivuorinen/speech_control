import logging
from autonomous_movement import obstacle_avoidance_main, stop_autonomous_movement
#from main import get_distance, check_obstacle
from motor_control import move_forward, move_backward, turn_left, turn_right, stop_motors
from video_stream import start_video_stream, stop_video_stream

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def execute_command(command):
    global obstacle_detected
    if command == "move forward":
        move_forward(0.7)
        logger.info("Moving forward")
    elif command == "move backward":
        move_backward(0.7)
        logger.info("Moving backwards")
    elif command == "turn left":
        turn_left(0.6)
        logger.info("Turning left")
    elif command == "turn right":
        turn_right(0.6)
        logger.info("Turning right")
    elif command == ("set free"):
        obstacle_avoidance_main()
        logger.info("Going freely")
    elif command == ("stop moving"):
        stop_autonomous_movement()
        logger.info("Stopping movement")
    elif command == ("start video"):
        start_video_stream()
        logger.info("Starting video stream")
    elif command == ("stop video"):
        stop_video_stream()
        logger.info("Stopping video stream")
    elif command == ("stop"):
        stop_motors()
        logger.info("Stopping")
    else:
        logger.warning(f"Unknown command: {command}")
        stop_motors()