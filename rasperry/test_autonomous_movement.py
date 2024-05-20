from autonomous_movement import start_obstacle_avoidance, stop_autonomous_movement
import time

if __name__ == '__main__':
    start_timer = time.time()  # Get the current time
    duration = 30  # duration in seconds

    # Start obstacle avoidance in a separate thread
    obstacle_avoidance_thread = start_obstacle_avoidance()

    # wait until the time has passed
    while time.time() - start_timer < duration:
        pass  # do nothing

    # After the specified duration, stop obstacle avoidance
    stop_autonomous_movement()
    obstacle_avoidance_thread.join()  # Wait for the obstacle avoidance thread to finish
