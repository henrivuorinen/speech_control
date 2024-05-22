from gpiozero import Motor, Robot
from time import sleep

# Create a Robot instance with the motor pins defined.
robot = Robot(left=Motor(9, 10), right=Motor(7, 8))

def move_forward(speed=1):
    """
    Function to move the vehicle forward.

    Args:
        speed (float, optional): Speed of movement, ranging from 0 to 1. Defaults to 1.
    """
    robot.forward(speed)

def move_backward(speed=1):
    """
    Function to move the vehicle backward.

    Args:
        speed (float, optional): Speed of movement, ranging from 0 to 1. Defaults to 1.
    """
    robot.backward(speed)

def turn_left(speed=1):
    """
    Function to turn the vehicle left.

    Args:
        speed (float, optional): Speed of turning, ranging from 0 to 1. Defaults to 1.
    """
    robot.left(speed)

def turn_right(speed=1):
    """
    Function to turn the vehicle right.

    Args:
        speed (float, optional): Speed of turning, ranging from 0 to 1. Defaults to 1.
    """
    robot.right(speed)

def stop_motors():
    """
    Function to stop all motors of the vehicle.
    """
    robot.stop()
