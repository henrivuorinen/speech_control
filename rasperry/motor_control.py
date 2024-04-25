from gpiozero import Motor, Robot
from time import sleep

# Create a Robot instance with the motor pins defined.
robot = Robot(left=Motor(7, 8), right=Motor(9, 10))

def move_forward(speed=1):
    robot.forward(speed)

def move_backward(speed=1):
    robot.backward(speed)

def turn_left(speed=1):
    robot.left(speed)

def turn_right(speed=1):
    robot.left(speed)

def stop_motors():
    robot.stop()

"""# Set the gpiozero pin factory to the pigpio implementation
Device.pin_factory = None  # use system's default pin factory

# Define GPIO pins for motor control
# Adjust these pin numbers according to your actual wiring
# Left wheel
IN1_LEFT = 7
IN2_LEFT = 8
# Right wheel
IN3_RIGHT = 9
IN4_RIGHT = 10

# Create motor objects for left and right motors
left_motor = Motor(forward=IN1_LEFT, backward=IN2_LEFT)
right_motor = Motor(forward=IN3_RIGHT, backward=IN4_RIGHT)

# Function to control motors
def control_motors(left_speed, right_speed):
    left_motor.value = left_speed / 100  # convert speed to a value between -1 and 1
    right_motor.value = right_speed / 100

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
    control_motors(speed, -speed)
    time.sleep(1)
    control_motors(speed, speed)
    time.sleep(0.5)
    stop_motors()

# Function to turn left
def turn_left(speed):
    control_motors(-speed, speed)
    time.sleep(1)
    control_motors(speed, speed)
    time.sleep(0.5)
    stop_motors()

# Function to stop motors
def stop_motors():
    left_motor.stop()
    right_motor.stop()"""
