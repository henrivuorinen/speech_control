import socket
import threading
import logging
from command_handler import execute_command

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_client(client_socket, addr):
    # Receive data from the client
    try:
        while True:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break
            logger.info(f"Received data from {addr}: {data}")

            # Extract the command from the received data
            command = data.strip()

            print(f"Received command: {command}")

            # Pass command to the execute_command function in main.py
            execute_command(command)

            # Send response back to the client
            response = f"Command '{command}' received and executed"
            client_socket.sendall(response.encode())
    except Exception as e:
        logger.error(f"Error handling client {addr}: {e}")
    finally:
        # Close the connection
        client_socket.close()
        logger.info(f"Closed connection with {addr}")

def start_server():
    # Set the IP address and port to listen on
    HOST = '0.0.0.0'  # Listen on all available network interfaces
    PORT = 12345

    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind the socket to the address and port
        server_socket.bind((HOST, PORT))

        # Listen for incoming connections
        server_socket.listen()

        logger.info(f"Server is listening on {HOST}:{PORT}")

        while True:
            # Accept a new connection
            client_socket, addr = server_socket.accept()
            logger.info(f"Connected by: {addr}")

            # Handle the client in a separate thread
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()

    except Exception as e:
        logger.error(f"Error starting server: {e}")
    finally:
        # Close the server socket when done
        server_socket.close()
