import speech_recognition as sr
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
    initialized = False

    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise once

        while True:
            print("Listening...")
            try:
                initialize_audio()
                audio = recognizer.listen(source, timeout=None)  # No timeout for this part
                if not initialized:
                    wake_word = recognizer.recognize_google(audio).lower()
                    if wake_word == "wake up":
                        play_sound(os.path.join("sounds", "start-test.wav"))
                        print("Wake word detected. Listening for commands")
                        initialized = True
                elif initialized:
                    command = recognizer.recognize_google(audio).lower()
                    print("Command detected: ", command)
                    yield command  # Return the command as a generator
            except sr.UnknownValueError:
                if initialized:
                    print("Failed to detect command. Retrying...")
                    play_error()
                    # Optionally, prompt the user to repeat the command
                    print("Please repeat the command.")
            except sr.RequestError as e:
                if initialized:
                    print(f"Error making the request; {e}")
                    play_error()
                    # Optionally, prompt the user to repeat the command
                    print("Please repeat the command.")

if __name__ == "__main__":
    initialize_audio()  # Initialize audio system before starting

    for command in listen_for_wake_word():
        if command == "move forward":
            # Your code to execute the "move forward" action
            print("Moving forward!")
            play_sound(os.path.join("sounds", "moving_forward.wav"))
        elif command == "shut down":
            print("Shutting down...")
            play_sound(os.path.join("sounds", "shut-down.wav"))
            break  # Exit the loop to stop the program
