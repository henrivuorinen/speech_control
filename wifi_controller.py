import socket
import logging

class WifiController:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.socket = None
        self.logger = logging.getLogger('wifi_controller')

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip_address, self.port))
            self.logger.info(f"Connected to {self.ip_address}:{self.port}:")
        except Exception as e:
            self.logger.error(f"Error connecting to {self.ip_address}:{self.port}: {e}")
            self.socket = None

    def send_data(self, data):
        if self.socket is None:
            self.logger.warning(f"Socket connection not established. Cannot send data")
            return

        try:
            self.socket.sendall(data.encode())
            self.logger.info(f"Data sent: {data}")
        except Exception as e:
            self.logger.error(f"Error sending data: {e}")

    def diconnect(self):
        if self.socket:
            self.socket.close()
            self.logger.info("Socker connection closed")
