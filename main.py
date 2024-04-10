import time
import os
from stream_voice_recognition import listen_for_wake_word, initialize_audio, play_sound
from wifi_controller import WifiController
import sys


def run_voice_control(wifi_controller):
    try:
        while True:
            command = listen_for_wake_word()
            initialize_audio()  # Initialize audio system

            if command == "move forward":
                # Your code to execute the "move forward" action
                print("Moving forward!")
                play_sound(os.path.join("sounds", "moving_forward.wav"))
                wifi_controller.send_data(command) # Send data to raspberry pi
            elif command == "move backward":

            elif command == "shut down":
                print("Shutting down...")
                play_sound(os.path.join("sounds", "shut-down.wav"))
                wifi_controller.send_data(command) # Send data to Raspberry Pi
                time.sleep(5)
                sys.exit()  # Stop the script
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Exiting...")


if __name__ == "__main__":
    raspberry_ip = "192.168.1.100" # Replace this with real one
    raspberry_port = 12345
    wifi_controller = WifiController(ip_address=raspberry_ip, port=raspberry_port)

    try:
        run_voice_control(wifi_controller)
    finally:
        wifi_controller.disconnect()
