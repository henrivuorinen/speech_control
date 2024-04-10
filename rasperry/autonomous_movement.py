import RPi.GPIO as GPIO
import time
from motor_control import move_forward, move_backward, turn_left, turn_right, stop_motors

# Set GPIO pins for ultrasound
TRIG_FRONT_PIN = 17
ECHO_FRONT_PIN = 18
TRIG_LEFT_PIN = 22
ECHO_LEFT_PIN = 23
TRIG_RIGHT_PIN = 24
ECHO_RIGHT_PIN = 25

# Set distance threshold
MAX_DISTANCE = 15

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_FRONT_PIN, GPIO.OUT)
GPIO.setup(ECHO_FRONT_PIN, GPIO.IN)
GPIO.setup(TRIG_LEFT_PIN, GPIO.OUT)
GPIO.setup(ECHO_LEFT_PIN, GPIO.IN)
GPIO.setup(TRIG_RIGHT_PIN, GPIO.OUT)
GPIO.setup(ECHO_RIGHT_PIN, GPIO.IN)

def stop_autonomous_movement():
    stop_motors()
    GPIO.cleanup()

def get_distance(trig_pin, echo_pin):
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig_pin, GPIO.LOW)

    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()

    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return distance

def stop_and_back():
    stop_motors()
    move_backward(50)
    time.sleep(1)
    stop_motors()

def avoid_obstacle():
    stop_motors()
    time.sleep(0.5)

    # Check distance in front, left, right
    distance_front = get_distance(TRIG_FRONT_PIN, ECHO_FRONT_PIN)
    distance_left = get_distance(TRIG_LEFT_PIN, ECHO_LEFT_PIN)
    distance_right = get_distance(TRIG_RIGHT_PIN, ECHO_RIGHT_PIN)

    # Determine the distance with most space
    if distance_front > MAX_DISTANCE:
        move_forward(50)
    elif distance_left > distance_right:
        turn_left(50)
    else:
        turn_right(50)

def obstacle_avoidance_main():
    try:
        while True:
            # Check distance and avoid obsticles
            distance_front = get_distance(TRIG_FRONT_PIN, ECHO_FRONT_PIN)
            if distance_front < MAX_DISTANCE:
                stop_and_back()
                avoid_obstacle()
            time.sleep(0.1)
    except KeyboardInterrupt:
        stop_motors()
    finally:
        GPIO.cleanup()