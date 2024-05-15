import threading
from time import sleep
import random
from motor_control import move_forward, move_backward, turn_left, turn_right, stop_motors
from gpiozero import DistanceSensor

sensor = DistanceSensor(echo=23, trigger=24, max_distance=1, threshold_distance=0.2)

#Global flag variable to control the running of autonomous movement
autonomous_movement_enabled = True

def stop_autonomous_movement():
    global autonomous_movement_enabled
    autonomous_movement_enabled = False
    stop_motors()

def stop_and_back():
    stop_motors()
    move_backward(0.7)
    sleep(1)
    stop_motors()

def avoid_obstacles():
    move_forward(0.7)  # Start moving forward
    sleep(0.5)   # Allow time for the car to start moving

    while autonomous_movement_enabled:
        # Check distance
        distance = sensor.distance
        print(f"Distance to obstacle: {distance: .2f} m")

        # Determine action based on distance
        if distance < sensor.max_distance:
            stop_motors()
            # Choose randomly left or right turn
            if random.choice([True, False]):
                turn_left(0.6)
            else:
                turn_right(0.6)
            # Check distance after turning
            sleep(0.5)
            distance = sensor.distance
            print(f"Distance after turning: {distance: .2f} cm")
            if distance < sensor.max_distance:
                # If still can't move, turn again
                if random.choice([True, False]):
                    turn_left(0.6)
                else:
                    turn_right(0.6)
        else:
            move_forward(0.7) #continue moving forward


def obstacle_avoidance_main():
    try:
        while autonomous_movement_enabled: #Check the flag before continuing
            avoid_obstacles()
            sleep(0.1)
    except KeyboardInterrupt:
        stop_motors()

def start_obstacle_avoidance():
    obstacle_avoidance_thread = threading.Thread(target=obstacle_avoidance_main)
    obstacle_avoidance_thread.start()

# Call this function to start obstacle avoidance in a separate thread
start_obstacle_avoidance()
