import time

import speech_recognition as sr
import sys
import pygame
import os


def initialize_audio():
    pygame.mixer.init()


def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()


def play_error():
    play_sound(os.path.join("sounds", "error.wav"))


def listen_for_wake_word():
    recognizer = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("Listening for wake word...")
            try:
                initialize_audio()  # Initialize audio system
                audio = recognizer.listen(source, timeout=500)  # Set a timeout (adjust as needed)
                wake_word = recognizer.recognize_google(audio).lower()
                if wake_word == "wake up":
                    play_sound(os.path.join("sounds", "start-test.wav"))
                    print("Wake word detected! Listening for command...")
                    return process_commands()
            except sr.UnknownValueError:
                print("Failed to detect wake word. Retrying...")
                play_error()
            except sr.RequestError as e:
                print(f"Error making the request; {e}")
                play_error()


def process_commands():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        initialize_audio()  # Initialize audio system
        print("Listening for command...")
        try:
            audio = recognizer.listen(source, timeout=5)  # Set a timeout (adjust as needed)
            command = recognizer.recognize_google(audio).lower()
            print("Command detected:", command)
            return command
        except sr.UnknownValueError:
            play_error()
            print("Failed to detect command. Retrying...")
        except sr.RequestError as e:
            play_error()
            print(f"Error making the request; {e}")


if __name__ == "__main__":
    # If you want to run this module independently for testing purposes
    command = listen_for_wake_word()
    initialize_audio()  # Initialize audio system

    if command == "move forward":
        # Your code to execute the "move forward" action
        print("Moving forward!")
        play_sound(os.path.join("sounds", "moving_forward.wav"))
    elif command == "shut down":
        print("Shutting down...")
        play_sound(os.path.join("sounds", "shut-down.wav"))
        sys.exit()  # Stop the script
