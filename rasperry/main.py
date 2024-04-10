import RPi.GPIO as GPIO
import time
import socket
import logging
import threading

from autonomous_movement import obstacle_avoidance_main
from motor_control import move_forward, move_backward, turn_left, turn_right, stop_motors
from server import start_server

# Import the function responsible for video streaming
from video_stream import video_stream

# Set the IP address and port of the server
SERVER_IP = "192.168.1.100"  # REPLACE THIS WITH THE IP ADDRESS OF THE RASP
SERVER_PORT = 12345  # REPLACE THIS WITH THE REAL PORT

# Set GPIO pins for ultrasound
TRIG_PIN = 17
ECHO_PIN = 18

# Set max distance threshold for obstacle detection
MAX_DISTANCE = 15

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Main")

def get_distance():
    # Trigger ultrasound sensor
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    # Measure the pulse duration from the echo pin
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    # Calculate distance
    distance = pulse_duration * 17150
    return distance

def connect_to_server(ip, port, timeout=100):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((ip, port))
        logger.info(f"Connected to server {ip}:{port}")
        return server_socket
    except Exception as e:
        logger.error(f"Error connecting to the server: {e}")
        return None

def recieve_command(server_socket):
    try:
        data = server_socket.recv(1024).decode("utf-8").strip()
        logger.info(f"Received command from server: {data}")
        return data
    except Exception as e:
        logger.error(f"Error receiving command from server: {e}")
        return None

def execute_command(command):
    if command == "move_forward":
        distance = get_distance()
        if distance < MAX_DISTANCE:
            move_forward(50)
            logger.info("Move forward")
        else:
            stop_motors()
            logger.info("Obstacle detected, stopping")
        move_forward(50)
    elif command == "move_backward":
        move_backward(50)
    elif command == "turn_left":
        turn_left(50)
    elif command == "turn_right":
        turn_right(50)
    elif command == "motors":
        stop_motors()
    else:
        logger.warning(f"Unknown command: {command}")

if __name__ == "__main__":
    # Initialize GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

    # Start obstacle avoidance thread
    avoidance_thread = threading.Thread(target=obstacle_avoidance_main)
    avoidance_thread.start()

    # Start server in a separate thread
    server_thread = threading.Thread(target=start_server())
    server_thread.start()

    # Start video streaming in a separate thread
    video_thread = threading.Thread(target=video_stream())
    video_thread.start()

    server_socket = connect_to_server(SERVER_IP, SERVER_PORT)
    if server_socket:
        try:
            while True:
                command = recieve_command(server_socket)
                if command:
                    execute_command(command)
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt")
        finally:
            server_socket.close()
            stop_motors()
            GPIO.cleanup()