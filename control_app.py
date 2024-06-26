import time
import os
from stream_voice_recognition import listen_for_wake_word, initialize_audio, play_sound
from wifi_controller import WifiController
from video_stream_recognition import VideoStreamRecognition
import sys

def send_written_message(wifi_controller, message):
    """
    Sends a written message to the Raspberry Pi via WiFi controller.

    Args:
        wifi_controller (WifiController): The WiFi controller instance.
        message (str): The message to send.
    """
    wifi_controller.send_data(message)
    print(f"Message sent to {wifi_controller}")

def run_voice_control(wifi_controller, video_capture):
    """
    Runs the voice control loop.

    Args:
        wifi_controller (WifiController): The WiFi controller instance.
        video_capture (VideoStreamRecognition): The video stream recognition instance.
    """
    try:
        # Connect to server
        wifi_controller.connect()

        # Initialize audio system
        initialize_audio()

        # Listen for wake word
        print("Waiting for the wake word")
        command_generator = listen_for_wake_word()

        # If wake word detected, enter command loop
        for command in command_generator:
            if command == "move forward":
                print("Moving forward!")
                play_sound(os.path.join("sounds", "moving_forward.wav"))
                wifi_controller.send_data(command)  # Send data to raspberry pi
                response = wifi_controller.receive_data()
                print("Response from server: ", response)
            elif command == "move backward":
                print("Moving backward!")
                wifi_controller.send_data(command)
                response = wifi_controller.receive_data()
                print("Response from server:", response)
            elif command == "turn left":
                print("turning left!")
                wifi_controller.send_data(command)
                response = wifi_controller.receive_data()
                print("Response from server:", response)
            elif command == "turn right":
                print("turning right!")
                wifi_controller.send_data(command)
                response = wifi_controller.receive_data()
                print("Response from server:", response)
            elif command == "stop":
                print("stopping!")
                wifi_controller.send_data(command)
                response = wifi_controller.receive_data()
                print("Response from server:", response)
            elif command == "set free":
                print("I set you free!")
                wifi_controller.send_data(command)
                response = wifi_controller.receive_data()
                print("Response from server:", response)
            elif command == "stop moving":
                print("I stopped moving!")
                wifi_controller.send_data(command)
                response = wifi_controller.receive_data()
                print("Response from server:", response)
            elif command == "send message":
                message = input(f"Enter the message here: ")
                send_written_message(wifi_controller, message)
                response = wifi_controller.receive_data()
                print("Response from server:", response)
            elif command == "dance":
                print("I dance!")
                wifi_controller.send_data(command)
                response = wifi_controller.receive_data()
                print("Response from server:", response)
            elif command == "start video":
                print("start recording")
                time.sleep(2)
                wifi_controller.send_data(command)
                video_capture.start()
                response = wifi_controller.receive_data()
                print("Response from server:", response)
            elif command == "stop video":
                print("stop recording")
                wifi_controller.send_data(command)
                video_capture.stop()
                response = wifi_controller.receive_data()
                print("Response from server:", response)
            elif command == "shut down":
                print("Shutting down...")
                play_sound(os.path.join("sounds", "shut-down.wav"))
                wifi_controller.send_data(command)  # Send data to Raspberry Pi
                response = wifi_controller.receive_data()
                print("Response from server:", response)
                time.sleep(5)
                break
            else:
                print("Unknown command:", command)

    except KeyboardInterrupt:
        print("KeyboardInterrupt: Exiting...")

if __name__ == "__main__":
    # Replace with actual Raspberry Pi IP and port
    raspberry_ip = "10.42.0.1"
    raspberry_port = 12345

    # Create a WiFi controller instance
    wifi_controller = WifiController(ip_address=raspberry_ip, port=raspberry_port)

    # Initialize the video stream
    video_capture = VideoStreamRecognition()

    try:
        run_voice_control(wifi_controller, video_capture)
    finally:
        # Disconnect WiFi controller and stop video capture on exit
        wifi_controller.disconnect()
        video_capture.stop()
