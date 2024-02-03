from bluetooth import BluetoothController
from stream_voice_recognition import listen_for_wake_word, initialize_audio, play_sound
import sys
import os

def run_voice_control(bluetooth_controller):
    try:
        while True:
            command = listen_for_wake_word()
            initialize_audio()  # Initialize audio system

            if command == "move forward":
                # Your code to execute the "move forward" action
                print("Moving forward!")
                play_sound(os.path.join("sounds", "moving_forward.wav"))
                bluetooth_controller.send_data(command)  # Send data to Arduino
            elif command == "shut down":
                print("Shutting down...")
                play_sound(os.path.join("sounds", "shutting_down.wav"))
                bluetooth_controller.send_data(command)  # Send data to Arduino
                sys.exit()  # Stop the script
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Exiting...")

if __name__ == "__main__":
    arduino_port = 'mock'  # Adjust the port as needed
    bluetooth_controller = BluetoothController(port=arduino_port)

    try:
        run_voice_control(bluetooth_controller)
    finally:
        bluetooth_controller.close_serial_port()
