import gpiozero
import time
import logging
#from autonomous_movement import obstacle_avoidance_main
#from main import get_distance, check_obstacle
from motor_control import move_forward, move_backward, turn_left, turn_right, stop_motors

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TRIG_PIN = 17
ECHO_PIN = 18

MAX_DISTANCE = 15

trig = gpiozero.OutputDevice(TRIG_PIN)
echo = gpiozero.DigitalInputDevice(ECHO_PIN)

def execute_command(command):
    global obstacle_detected
    if command == "move forward":
        #check_obstacle()
        if not obstacle_detected:
            move_forward(50)
            logger.info("Moving forward")
        else:
            stop_motors()
            logger.info("Obstacle detected")
    elif command == "move backward":
        move_forward(50)
        logger.info("Moving backwards")
    elif command == "turn left":
        turn_left(50)
        logger.info("Turning left")
    elif command == "turn right":
        turn_right(50)
        logger.info("Turning right")
    #elif command == ("set free"):
    #    obstacle_avoidance_main()
        logger.info("Going freely")
    elif command == ("stop"):
        stop_motors()
        logger.info("Stopping")
    else:
        logger.warning(f"Unknown command: {command}")
        stop_motors()