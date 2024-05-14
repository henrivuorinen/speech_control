from autonomous_movement import obstacle_avoidance_main
import time

if __name__ == '__main__':
    start_timer = time.time() #Get the current time
    duration = 30 #duration in seconds

    #start obstacle avoidance in separate thread
    obstacle_avoidance_thread = obstacle_avoidance_main()

    # wait until the time has passed
    while time.time() - start_timer < duration:
        pass # do nothing

    # After the specified duration, stop obstacle avoidance
    obstacle_avoidance_thread.join()  # Wait for the obstacle avoidance thread to finish