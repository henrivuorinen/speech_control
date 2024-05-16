import logging
import socket
import threading
from time import sleep
from gpiozero import Robot, Motor, DistanceSensor

from command_handler import execute_command
from autonomous_movement import obstacle_avoidance_main
from motor_control import move_forward, move_backward, turn_left, turn_right, stop_motors
from video_stream import start_video_stream, stop_video_stream

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

def receive_command(server_socket):
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
            stop_motors()
            logger.info("Obstacle detected. Stopping motors.")
            sleep(0.5)
            move_backward(1)
            sleep(0.5)
            turn_right(1)
        sleep(0.5)

def handle_client(client_socket, addr):
    try:
        while True:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break
            logger.info(f"Received data from {addr}: {data}")

            command = data.strip()
            print(f"Received command: {command}")
            execute_command(command)

            response = f"Command '{command}' received and executed"
            client_socket.sendall(response.encode())
    except Exception as e:
        logger.error(f"Error handling client {addr}: {e}")
    finally:
        client_socket.close()
        logger.info(f"Closed connection with {addr}")

def start_command_server():
    HOST = '0.0.0.0'
    PORT = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        logger.info(f"Command server is listening on {HOST}:{PORT}")

        while True:
            client_socket, addr = server_socket.accept()
            logger.info(f"Connected by: {addr}")

            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()
    except Exception as e:
        logger.error(f"Error starting command server: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    # Start the command server in a separate thread
    command_server_thread = threading.Thread(target=start_command_server)
    command_server_thread.start()

    # Start the distance sensor handler in a separate thread
    distance_sensor_thread = threading.Thread(target=distance_sensor_handler)
    distance_sensor_thread.start()

    server_socket = connect_to_server(SERVER_IP, SERVER_PORT)
    if server_socket:
        try:
            while True:
                command = receive_command(server_socket)
                if command:
                    if command == "start video":
                        start_video_stream()
                    elif command == "stop video":
                        stop_video_stream()
                    else:
                        execute_command(command)
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt")
        finally:
            server_socket.close()
            stop_motors()
            stop_video_stream()
