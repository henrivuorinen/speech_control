import serial
import serial.tools.list_ports
import logging

class BluetoothController:
    def __init__(self, port=None, baud_rate=9600):
        self.baud_rate = baud_rate
        self.ser = None  # Initialize to None

        if port is not None:
            self.open_serial_port(port)
        else:
            self.open_serial_port()

        self.logger = logging.getLogger("BluetoothController")

    def open_serial_port(self, port):
        if port == 'mock':
            # Use a mock serial class for testing
            self.ser = MockSerial()
            print("Mock serial port opened.")
            return

        available_ports = [port.device for port in serial.tools.list_ports.comports()]
        if not available_ports:
            self.logger.error("No available serial ports")
            return False

        # Choose the first available port (you may need to adapt this logic based on your setup)
        chosen_port = available_ports[0]

        try:
            self.ser = serial.Serial(chosen_port, self.baud_rate, timeout=1)
            self.logger.info(f"Serial port opened: {chosen_port}")
            return True
        except serial.SerialException as e:
            self.logger.error(f"Error opening serial port: {e}")
            self.ser = None
            return False

    def send_data(self, data):
        if self.ser is None:
            self.logger.warn("Serial port not open. Can't send data")
            return

        try:
            self.ser.write(data.encode())
        except serial.SerialException as e:
            self.logger.error(f"Error sending data over serial port: {e}")

    def close_serial_port(self):
        if self.ser is not None:
            self.ser.close()
            self.logger.info("Serial port closed")


class MockSerial:
    def __init__(self):
        self.data_buffer = b""
        #Add logger attribute
        self.logger = logging.getLogger("MockSerial") 

    def write(self, data):
        self.logger.info(f"MockSerial: Data sent: {data}")
        # You can simulate the behavior of the Arduino response in the mock class
        self.data_buffer += data
        if b"\n" in self.data_buffer:
            received_data, self.data_buffer = self.data_buffer.split(b"\n", 1)
            self.logger.info(f"MockSerial: Data recieved: {received_data.decode()}")

    def close(self):
        self.logger.info("MockSerial: Closed")
