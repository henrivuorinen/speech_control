from gpiozero import Robot, Motor, DistanceSensor
from time import sleep
import socket
import logging
import threading

from command_handler import execute_command
from autonomous_movement import obstacle_avoidance_main
from motor_control import move_forward, move_backward, turn_left, turn_right, stop_motors
from server import start_server

# Import the function responsible for video streaming
from video_stream import video_stream, start_video_stream, stop_video_stream

# Set the IP address and port of the server
SERVER_IP = "10.42.0.1"  # REPLACE THIS WITH THE IP ADDRESS OF THE RASP
SERVER_PORT = 12345  # REPLACE THIS WITH THE REAL PORT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Main")

robot = Robot(left=Motor(7, 8), right=Motor(9, 10))
sensor = DistanceSensor(23, 24, max_distance=1, threshold_distance=0.2)

def connect_to_server(ip, port, timeout=100):
    global server_socket
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


def distance_sensor_handler():
    while True:
        if sensor.distance < 0.2:
            # Trigger action when an obstacle is detected
            stop_motors()
            logger.info("Obstacle detected. Stopping motors.")
            sleep(0.5)
            move_backward(1)
            sleep(0.5)
            turn_right(1)
        sleep(0.5)



if __name__ == "__main__":
    # Start server and video streaming in separate threads
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    video_thread = threading.Thread(target=start_video_stream)
    video_thread.start()

    server_socket = connect_to_server(SERVER_IP, SERVER_PORT)
    if server_socket:
        try:
            # Start obstacle avoidance mechanism in a separate thread
            #obstacle_avoidance_thread = threading.Thread(target=obstacle_avoidance_main)
            #obstacle_avoidance_thread.start()

            while True:
                # Execute commands
                command = recieve_command(server_socket)
                if command:
                    execute_command(command)

        except KeyboardInterrupt:
            logger.info("Keyboard interrupt")
        finally:
            server_socket.close()
            stop_motors()
