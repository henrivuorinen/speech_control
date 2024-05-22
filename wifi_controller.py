import socket
import logging

class WifiController:
    def __init__(self, ip_address, port):
        """
        Initializes the WifiController with the IP address and port.

        Args:
            ip_address (str): The IP address of the Raspberry Pi.
            port (int): The port number to connect to on the Raspberry Pi.
        """
        self.ip_address = ip_address
        self.port = port
        self.socket = None
        self.logger = logging.getLogger('wifi_controller')

    def connect(self):
        """
        Connects to the Raspberry Pi over Wi-Fi.
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip_address, self.port))
            self.logger.info(f"Connected to {self.ip_address}:{self.port}:")
        except Exception as e:
            self.logger.error(f"Error connecting to {self.ip_address}:{self.port}: {e}")
            self.socket = None

    def send_data(self, data):
        """
        Sends data to the Raspberry Pi.

        Args:
            data (str): The data to be sent.
        """
        if self.socket is None:
            self.logger.warning(f"Socket connection not established. Cannot send data")
            return

        try:
            self.socket.sendall(data.encode())
            self.logger.info(f"Data sent: {data}")
        except Exception as e:
            self.logger.error(f"Error sending data: {e}")

    def receive_data(self):
        """
        Receives data from the Raspberry Pi.

        Returns:
            str: The received data.
        """
        if self.socket is None:
            self.logger.warning(f"Socket connection not established. Cannot receive data")
            return None
        try:
            received_data = self.socket.recv(1024).decode('utf-8').strip()
            self.logger.info(f"Data received: {received_data}")
            return received_data
        except Exception as e:
            self.logger.error(f"Error receiving data: {e}")
            return None

    def disconnect(self):
        """
        Disconnects from the Raspberry Pi.
        """
        if self.socket:
            self.socket.close()
            self.logger.info("Socket connection closed")
