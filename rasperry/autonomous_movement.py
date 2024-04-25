import threading
from time import sleep
import random
from motor_control import move_forward, move_backward, turn_left, turn_right, stop_motors
from gpiozero import DistanceSensor

sensor = DistanceSensor(echo=23, trigger=24, max_distance=1, threshold_distance=0.2)

def stop_autonomous_movement():
    stop_motors()

def stop_and_back():
    stop_motors()
    move_backward(50)
    sleep(1)
    stop_motors()

def avoid_obstacles():
    move_forward()  # Start moving forward
    sleep(0.5)   # Allow time for the car to start moving

    while True:
        # Check distance
        distance = sensor.distance
        print(f"Distance to obstacle: {distance: .2f} cm")

        # Determine action based on distance
        if distance < sensor.max_distance:
            stop_motors()
            # Choose randomly left or right turn
            if random.choice([True, False]):
                turn_left(50)
            else:
                turn_right(50)
            # Check distance after turning
            sleep(0.5)
            distance = sensor.distance
            print(f"Distance after turning: {distance: .2f} cm")
            if distance < sensor.max_distance:
                # If still can't move, turn again
                if random.choice([True, False]):
                    turn_left(50)
                else:
                    turn_right(50)


def obstacle_avoidance_main():
    try:
        while True:
            avoid_obstacles()
            sleep(0.1)
    except KeyboardInterrupt:
        stop_motors()

def start_obstacle_avoidance():
    obstacle_avoidance_thread = threading.Thread(target=obstacle_avoidance_main)
    obstacle_avoidance_thread.start()

# Call this function to start obstacle avoidance in a separate thread
start_obstacle_avoidance()
