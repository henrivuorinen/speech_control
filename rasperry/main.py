import socket
import logging
import threading

# Import functions from other modules
from command_handler import execute_command
from autonomous_movement import obstacle_avoidance_main
from motor_control import move_forward, move_backward, turn_left, turn_right, stop_motors
from server import start_server

# Import the function responsible for video streaming
from video_stream import video_stream, start_video_stream, stop_video_stream

# Set the IP address and port of the server
SERVER_IP = "10.42.0.1"  # REPLACE THIS WITH THE IP ADDRESS OF THE RASPBERRY PI
SERVER_PORT = 12345  # REPLACE THIS WITH THE REAL PORT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Main")

def connect_to_server(ip, port, timeout=100):
    """
    Function to connect to the server.

    Args:
        ip (str): IP address of the server.
        port (int): Port of the server.
        timeout (int, optional): Connection timeout in seconds. Defaults to 100.

    Returns:
        socket.socket: Socket object representing the connection to the server, or None if connection failed.
    """
    global server_socket
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((ip, port))
        logger.info(f"Connected to server {ip}:{port}")
        return server_socket
    except Exception as e:
        logger.error(f"Error connecting to the server: {e}")
        return None

def receive_command(server_socket):
    """
    Function to receive commands from the server.

    Args:
        server_socket (socket.socket): Socket object representing the connection to the server.

    Returns:
        str: Received command from the server, or None if no command received.
    """
    try:
        data = server_socket.recv(1024).decode("utf-8").strip()
        logger.info(f"Received command from server: {data}")
        return data
    except Exception as e:
        logger.error(f"Error receiving command from server: {e}")
        return None

"""def distance_sensor_handler():
    while True:
        if sensor.distance < 0.2:
            # Trigger action when an obstacle is detected
            stop_motors()
            logger.info("Obstacle detected. Stopping motors.")
            sleep(0.5)
            move_backward(1)
            sleep(0.5)
            turn_right(1)
        sleep(0.5)"""


if __name__ == "__main__":
    # Start server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # Connect to the server
    server_socket = connect_to_server(SERVER_IP, SERVER_PORT)
    if server_socket:
        try:
            # Start video streaming in a separate thread if the command is received
            video_thread = None
            while True:
                command = receive_command(server_socket)
                if command:
                    if command == "start video" and not video_thread:
                        video_thread = threading.Thread(target=start_video_stream)
                        video_thread.start()
                    elif command == "stop video" and video_thread:
                        stop_video_stream()
                        video_thread.join()
                        video_thread = None
                    else:
                        execute_command(command)
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt")
        finally:
            # Close the connection and stop motors and video streaming
            server_socket.close()
            stop_motors()
            stop_video_stream()
            if video_thread:
                video_thread.join()
