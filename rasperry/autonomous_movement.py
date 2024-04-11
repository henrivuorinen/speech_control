from gpiozero import DistanceSensor
import time
import random
from motor_control import move_forward, move_backward, turn_left, turn_right, stop_motors

# Set distance sensor pins
TRIG_PIN = 4
ECHO_PIN = 17

# Set distance threshold
MAX_DISTANCE = 15 # Adjust if needed

sensor_front = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN)

def stop_autonomous_movement():
    stop_motors()

def stop_and_back():
    stop_motors()
    move_backward(50)
    time.sleep(1)
    stop_motors()

def avoid_obstacles():
    stop_motors()
    time.sleep(0.5)

    # Check distance
    distance = sensor_front.distance

    # Determin action based on distance
    if distance < MAX_DISTANCE:
        stop_motors()
        # Choose randomly left or right turn
        if random.choice([True, False]):
            turn_left(50)
        else:
            turn_right(50)
        # Check distance after turning
        time.sleep(0.5)
        distance = sensor_front.distance
        if distance < MAX_DISTANCE:
            # If still cant move, turn again
            if random.choice([True, False]):
                turn_left(50)
            else:
                turn_right(50)

def obstacle_avoidance_main():
    try:
        while True:
            avoid_obstacles()
            time.sleep(0.1)
    except KeyboardInterrupt:
        stop_motors()
