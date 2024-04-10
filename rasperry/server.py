import socket

def start_server():
    # Set the IP address and port to listen on
    HOST = '0.0.0.0' # Listen on all available network interfaces
    PORT = 12345

    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen()

    print(f"Server is listening on {HOST}:{PORT}")

    while True:
        # Accept a new connection
        client_socket, addr = server_socket.accept()
        print(f"Connected by: {addr}")

        # Receive data
        data = client_socket.recv(1024).decode().strip()

        # Process the received data

        # Send response back
        response = "Data received"
        client_socket.sendall(response.encode())

        # Close the connection
        client_socket.close()
