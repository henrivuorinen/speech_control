import time
import os
from stream_voice_recognition import listen_for_wake_word, initialize_audio, play_sound
from wifi_controller import WifiController
from video_stream_recognition import VideoStreamRecognition
import sys


def send_written_message(wifi_controller, message):
    wifi_controller.send_data(message)
    print(f"Message sent to {wifi_controller}")

def run_voice_control(wifi_controller):
    try:
        # Connect to server
        wifi_controller.connect()
        while True:
            command = listen_for_wake_word()
            initialize_audio()  # Initialize audio system

            if command == "move forward":
                print("Moving forward!")
                play_sound(os.path.join("sounds", "moving_forward.wav"))
                wifi_controller.send_data(command) # Send data to raspberry pi
            elif command == "move backward":
                print("Moving backward!")
                wifi_controller.send_data(command)
                response = wifi_controller.receive_data()
                print("Response from server:", response)
            elif command == "turn left":
                print("turning left!")
                wifi_controller.send_data(command)
            elif command == "turn right":
                print("turning right!")
                wifi_controller.send_data(command)
            elif command == "stop":
                print("stopping!")
                wifi_controller.send_data(command)
            elif command == "i set you free":
                print("I set you free!")
                wifi_controller.send_data(command)
            elif command == "send message":
                message = input(f"Enter the message here: ")
                send_written_message(wifi_controller, message)
            elif command == "start video":
                print("start recording")
                video_capture.start()
            elif command == "stop video":
                print("stop recording")
                video_capture.stop()
            elif command == "shut down":
                print("Shutting down...")
                play_sound(os.path.join("sounds", "shut-down.wav"))
                wifi_controller.send_data(command) # Send data to Raspberry Pi
                time.sleep(5)
                sys.exit()  # Stop the script
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Exiting...")


if __name__ == "__main__":
    raspberry_ip = "192.168.1.195" # Replace this with real one
    raspberry_port = 12345
    wifi_controller = WifiController(ip_address=raspberry_ip, port=raspberry_port)

    # Initialize the video stream
    video_capture = VideoStreamRecognition()

    try:
        run_voice_control(wifi_controller)
    finally:
        wifi_controller.disconnect()
