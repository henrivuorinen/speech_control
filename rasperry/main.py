import gpiozero
import time
import socket
import logging
import threading

from command_handler import execute_command
#from autonomous_movement import obstacle_avoidance_main
from motor_control import move_forward, move_backward, turn_left, turn_right, stop_motors
from server import start_server

# Import the function responsible for video streaming
# from video_stream import video_stream, start_video_stream, stop_video_stream

# Set the IP address and port of the server
SERVER_IP = "192.168.1.100"  # REPLACE THIS WITH THE IP ADDRESS OF THE RASP
SERVER_PORT = 12345  # REPLACE THIS WITH THE REAL PORT

# Set GPIO pins for ultrasound
#TRIG_PIN = 4
#ECHO_PIN = 17

# Set max distance threshold for obstacle detection
MAX_DISTANCE = 15

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Main")

obstacle_detected = False

# Initialize GPIO
#trig = gpiozero.OutputDevice(TRIG_PIN)
#echo = gpiozero.DigitalInputDevice(ECHO_PIN)

"""def get_distance():
    # Trigger ultrasound sensor
    trig.on()
    time.sleep(0.00001)
    trig.off()

    # Measure the pulse duration from the echo pin
    pulse_start = time.time()
    while not echo.is_active:
        pulse_start = time.time()

    pulse_end = time.time()
    while echo.is_active:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    # Calculate distance
    distance = pulse_duration * 17150
    return distance


def check_obstacle():
    global obstacle_detected
    distance = get_distance()
    if distance < MAX_DISTANCE:
        obstacle_detected = True
    else:
        obstacle_detected = False"""


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


def main_loop():
    global obstacle_detected
    while True:
        # Check obstacles
        #check_obstacle()

        # Execute commands
        command = recieve_command(server_socket)
        if command:
            execute_command(command)


if __name__ == "__main__":
    # Start server in a separate thread
    server_thread = threading.Thread(target=start_server())
    server_thread.start()

    # Start video streaming in a separate thread
    # video_thread = threading.Thread(target=start_video_stream)
    # video_thread.start()

    server_socket = connect_to_server(SERVER_IP, SERVER_PORT)
    if server_socket:
        try:
            main_loop()
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt")
        finally:
            server_socket.close()
            stop_motors()
