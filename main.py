from bluetooth import BluetoothController
from voice_recognition import recognize_speech

def run_voice_control():
    # Specify 'mock' as the port for testing without a physical serial port
    bluetooth_controller = BluetoothController(port='mock')

    while True:
        command = recognize_speech()
        if command:
            bluetooth_controller.send_data(command)

if __name__ == "__main__":
    run_voice_control()
