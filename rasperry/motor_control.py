import RPi.GPIO as GPIO
import time

# Define GPIO pins for motor control
# Adjust these pin numbers according to your actual wiring
# Left wheel
IN1_LEFT = 7
IN2_LEFT = 8
# Right wheel
IN3_RIGHT = 9
IN4_RIGHT = 10

# Setup GPIO mode and pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1_LEFT, GPIO.OUT)
GPIO.setup(IN2_LEFT, GPIO.OUT)
GPIO.setup(IN3_RIGHT, GPIO.OUT)
GPIO.setup(IN4_RIGHT, GPIO.OUT)

# Function to control motor direction and speed
def control_motors(left_speed, right_speed):
    # Left motor control
    if left_speed > 0:
        GPIO.output(IN1_LEFT, GPIO.HIGH)
        GPIO.output(IN2_LEFT, GPIO.LOW)
    elif left_speed < 0:
        GPIO.output(IN1_LEFT, GPIO.LOW)
        GPIO.output(IN2_LEFT, GPIO.HIGH)
    else:
        GPIO.output(IN1_LEFT, GPIO.LOW)
        GPIO.output(IN2_LEFT, GPIO.LOW)

    # Right motor control
    if right_speed > 0:
        GPIO.output(IN3_RIGHT, GPIO.HIGH)
        GPIO.output(IN4_RIGHT, GPIO.LOW)
    elif right_speed < 0:
        GPIO.output(IN3_RIGHT, GPIO.LOW)
        GPIO.output(IN4_RIGHT, GPIO.HIGH)
    else:
        GPIO.output(IN3_RIGHT, GPIO.LOW)
        GPIO.output(IN4_RIGHT, GPIO.LOW)

    # Adjust this part for speed control (using PWM)
    # Example: pwm_left = GPIO.PWM(IN1_LEFT, 100)  # 100 Hz frequency
    #          pwm_left.start(abs(left_speed))     # Start PWM with left motor speed
    #          pwm_right = GPIO.PWM(IN3_RIGHT, 100)  # 100 Hz frequency
    #          pwm_right.start(abs(right_speed))    # Start PWM with right motor speed

# Function to move forward
def move_forward(speed):
    control_motors(speed, speed)
    time.sleep(5)
    stop_motors()

# Function to move backward
def move_backward(speed):
    control_motors(-speed, -speed)
    time.sleep(5)
    stop_motors()

# Function to turn right
def turn_right(speed):
    control_motors(0, -speed)
    time.sleep(1)
    control_motors(speed, -speed)
    time.sleep(0.5)
    stop_motors()

# Function to turn left
def turn_left(speed):
    control_motors(-speed, 0)
    time.sleep(1)
    control_motors(speed, -speed)
    time.sleep(0.5)
    stop_motors()

# Function to stop motors and cleanup GPIO
def stop_motors():
    GPIO.output(IN1_LEFT, GPIO.LOW)
    GPIO.output(IN2_LEFT, GPIO.LOW)
    GPIO.output(IN3_RIGHT, GPIO.LOW)
    GPIO.output(IN4_RIGHT, GPIO.LOW)
    GPIO.cleanup()
