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

